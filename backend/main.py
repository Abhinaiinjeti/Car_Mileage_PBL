"""
AutoMileage AI - FastAPI Backend Server
Serves cascading vehicle selectors, model predictions, and ML metrics.
"""

import os
import json
import sqlite3
import joblib
import pandas as pd
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODEL_DIR = os.path.join(BASE_DIR, "model")
DB_PATH = os.path.join(DATA_DIR, "vehicles_catalog.db")
PIPELINE_PATH = os.path.join(MODEL_DIR, "random_forest_pipeline.pkl")
METRICS_PATH = os.path.join(MODEL_DIR, "metrics.json")

# 1 MPG = 0.425144 km/L
MPG_TO_KMPL = 0.425144

app = FastAPI(
    title="AutoMileage AI API",
    description="Machine Learning Fuel Mileage Prediction API using Random Forest Regression on official EPA vehicle data.",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model cache
pipeline = None
metrics_data = None

def get_db_connection():
    if not os.path.exists(DB_PATH):
        raise HTTPException(status_code=503, detail="Vehicle catalog database not found. Please train model first.")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def load_ml_pipeline():
    global pipeline
    if pipeline is None:
        if not os.path.exists(PIPELINE_PATH):
            raise RuntimeError(f"Trained model not found at {PIPELINE_PATH}. Please run train_model.py first.")
        pipeline = joblib.load(PIPELINE_PATH)
    return pipeline

def load_metrics():
    global metrics_data
    if metrics_data is None:
        if os.path.exists(METRICS_PATH):
            with open(METRICS_PATH, "r") as f:
                metrics_data = json.load(f)
        else:
            metrics_data = {}
    return metrics_data

@app.on_event("startup")
def startup_event():
    try:
        load_ml_pipeline()
        load_metrics()
        print("[OK] Loaded ML pipeline and metrics successfully.")
    except Exception as e:
        print(f"[WARNING] Startup initialization notice: {e}")

class PredictRequest(BaseModel):
    vehicle_id: Optional[int] = Field(None, description="Direct ID of vehicle from catalog")
    year: Optional[int] = Field(None, description="Model Year")
    make: Optional[str] = Field(None, description="Vehicle Brand / Make")
    model: Optional[str] = Field(None, description="Vehicle Model")
    variant: Optional[str] = Field(None, description="Selected Variant String")

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "AutoMileage AI Backend",
        "model_loaded": pipeline is not None,
        "database_available": os.path.exists(DB_PATH)
    }

@app.get("/api/years")
def get_years():
    """Retrieve distinct vehicle model years sorted descending."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT year FROM vehicles WHERE year >= 1990 ORDER BY year DESC")
        rows = cursor.fetchall()
        conn.close()
        return [row["year"] for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving years: {str(e)}")

@app.get("/api/makes")
def get_makes(year: int = Query(..., description="Selected model year")):
    """Retrieve available vehicle makes/brands for the given year."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT DISTINCT make FROM vehicles WHERE year = ? ORDER BY make ASC",
            (year,)
        )
        rows = cursor.fetchall()
        conn.close()
        return [row["make"] for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving makes: {str(e)}")

@app.get("/api/models")
def get_models(
    year: int = Query(..., description="Selected model year"),
    make: str = Query(..., description="Selected vehicle brand/make")
):
    """Retrieve available vehicle models for the selected year and make."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT DISTINCT model FROM vehicles WHERE year = ? AND make = ? ORDER BY model ASC",
            (year, make)
        )
        rows = cursor.fetchall()
        conn.close()
        return [row["model"] for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving models: {str(e)}")

@app.get("/api/variants")
def get_variants(
    year: int = Query(..., description="Selected model year"),
    make: str = Query(..., description="Selected vehicle brand/make"),
    model: str = Query(..., description="Selected vehicle model")
):
    """Retrieve valid vehicle variants/configurations for the selected vehicle."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, year, make, model, variant, displ, cylinders, trany, drive, fuelType1, VClass
            FROM vehicles
            WHERE year = ? AND make = ? AND model = ?
            ORDER BY displ ASC, cylinders ASC, trany ASC
        """, (year, make, model))
        rows = cursor.fetchall()
        conn.close()

        variants = []
        for r in rows:
            variants.append({
                "id": r["id"],
                "variant": r["variant"],
                "displ": r["displ"],
                "cylinders": r["cylinders"],
                "trany": r["trany"],
                "drive": r["drive"],
                "fuelType1": r["fuelType1"],
                "vclass": r["VClass"]
            })
        return variants
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving variants: {str(e)}")

def get_efficiency_rating(kmpl: float) -> str:
    """Categorize fuel efficiency in clear, human-understandable terms."""
    if kmpl >= 17.0:
        return "Exceptional Efficiency"
    elif kmpl >= 13.0:
        return "Good Estimated Efficiency"
    elif kmpl >= 10.0:
        return "Moderate Efficiency"
    else:
        return "Higher Fuel Consumption"

@app.post("/api/predict")
def predict_mileage(req: PredictRequest):
    """
    Accepts vehicle selection, retrieves true vehicle specifications from catalog,
    feeds them through the trained Random Forest pipeline, and computes predicted MPG and km/L.
    """
    ml_model = load_ml_pipeline()
    
    conn = get_db_connection()
    cursor = conn.cursor()

    vehicle_row = None
    if req.vehicle_id is not None:
        cursor.execute("SELECT * FROM vehicles WHERE id = ?", (req.vehicle_id,))
        vehicle_row = cursor.fetchone()
    elif req.year and req.make and req.model:
        if req.variant:
            cursor.execute(
                "SELECT * FROM vehicles WHERE year = ? AND make = ? AND model = ? AND variant = ? LIMIT 1",
                (req.year, req.make, req.model, req.variant)
            )
            vehicle_row = cursor.fetchone()
        if not vehicle_row:
            cursor.execute(
                "SELECT * FROM vehicles WHERE year = ? AND make = ? AND model = ? LIMIT 1",
                (req.year, req.make, req.model)
            )
            vehicle_row = cursor.fetchone()
    
    conn.close()

    if not vehicle_row:
        raise HTTPException(status_code=404, detail="Vehicle specifications not found for the given selection.")

    # Prepare features for ML Model (MUST match ALL_FEATURES from training)
    features_df = pd.DataFrame([{
        "year": int(vehicle_row["year"]),
        "displ": float(vehicle_row["displ"]),
        "cylinders": float(vehicle_row["cylinders"]),
        "drive": str(vehicle_row["drive"]),
        "trany": str(vehicle_row["trany"]),
        "fuelType1": str(vehicle_row["fuelType1"]),
        "VClass": str(vehicle_row["VClass"])
    }])

    # Run Random Forest Regression
    try:
        pred_mpg = float(ml_model.predict(features_df)[0])
        pred_mpg = max(5.0, round(pred_mpg, 1))
        pred_kmpl = round(pred_mpg * MPG_TO_KMPL, 1)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ML Prediction calculation error: {str(e)}")

    efficiency_rating = get_efficiency_rating(pred_kmpl)

    # Format user-friendly specification values
    displ_val = float(vehicle_row["displ"])
    cyl_val = int(vehicle_row["cylinders"])
    engine_str = f"{displ_val:.1f} L" if displ_val > 0 else "Electric Motor"
    cyl_str = f"{cyl_val} Cylinders" if cyl_val > 0 else "N/A (Electric)"

    return {
        "vehicle": f"{vehicle_row['year']} {vehicle_row['make']} {vehicle_row['model']}",
        "variant": vehicle_row["variant"],
        "year": int(vehicle_row["year"]),
        "make": vehicle_row["make"],
        "model": vehicle_row["model"],
        "predicted_mpg": pred_mpg,
        "predicted_kmpl": pred_kmpl,
        "efficiency_rating": efficiency_rating,
        "specs": {
            "engine": engine_str,
            "cylinders": cyl_str,
            "transmission": vehicle_row["trany"],
            "fuel_type": vehicle_row["fuelType1"],
            "drive_type": vehicle_row["drive"],
            "vehicle_class": vehicle_row["VClass"]
        },
        "conversion_standard": "1 MPG = 0.425144 km/L"
    }

@app.get("/api/model-insights")
def get_model_insights():
    """Returns actual trained model metrics, feature importances, and sample test predictions."""
    metrics = load_metrics()
    if not metrics:
        raise HTTPException(status_code=503, detail="Model metrics not yet computed.")
    return metrics

# Mount Built React Frontend if dist exists (allowing turnkey single-server execution)
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

FRONTEND_DIST = os.path.join(os.path.dirname(BASE_DIR), "frontend", "dist")
ASSETS_DIR = os.path.join(FRONTEND_DIST, "assets")

if os.path.exists(ASSETS_DIR):
    app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")

if os.path.exists(FRONTEND_DIST):
    @app.get("/{full_path:path}")
    async def serve_frontend_spa(full_path: str):
        if full_path.startswith("api"):
            raise HTTPException(status_code=404, detail="API endpoint not found")
        target_path = os.path.join(FRONTEND_DIST, full_path)
        if os.path.exists(target_path) and os.path.isfile(target_path):
            return FileResponse(target_path)
        return FileResponse(os.path.join(FRONTEND_DIST, "index.html"))

