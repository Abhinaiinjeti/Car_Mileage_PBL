"""
AutoMileage AI - Model Training Pipeline
Trains a Random Forest Regressor on the official U.S. EPA FuelEconomy.gov dataset.
Computes real evaluation metrics (MAE, RMSE, R2), feature importances,
and test-set actual vs predicted points. Builds the vehicle lookup catalog.
"""

import os
import sys
import json
import sqlite3
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODEL_DIR = os.path.join(BASE_DIR, "model")
CSV_PATH = os.path.join(DATA_DIR, "vehicles.csv")
DB_PATH = os.path.join(DATA_DIR, "vehicles_catalog.db")
PIPELINE_PATH = os.path.join(MODEL_DIR, "random_forest_pipeline.pkl")
METRICS_PATH = os.path.join(MODEL_DIR, "metrics.json")

# Features to use (strictly mechanical / engineering specifications - NO TARGET LEAKAGE)
NUMERIC_FEATURES = ['year', 'displ', 'cylinders']
CATEGORICAL_FEATURES = ['drive', 'trany', 'fuelType1', 'VClass']
ALL_FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES
TARGET = 'comb08'  # Combined MPG for fuelType1

def format_variant_title(row):
    """Generate a clean, descriptive variant string for users."""
    parts = []
    if pd.notna(row.get('cylinders')) and row.get('cylinders', 0) > 0:
        parts.append(f"{int(row['cylinders'])} cyl")
    if pd.notna(row.get('displ')) and row.get('displ', 0) > 0:
        parts.append(f"{float(row['displ']):.1f}L")
    if pd.notna(row.get('trany')) and str(row.get('trany')).strip():
        parts.append(str(row['trany']).strip())
    if pd.notna(row.get('drive')) and str(row.get('drive')).strip():
        parts.append(str(row['drive']).strip())
    if pd.notna(row.get('fuelType1')) and str(row.get('fuelType1')).strip():
        fuel = str(row['fuelType1']).strip()
        if "Electricity" in fuel:
            parts.append("Electric")
        elif "Diesel" in fuel:
            parts.append("Diesel")
    return " | ".join(parts) if parts else "Standard Configuration"

def train():
    os.makedirs(MODEL_DIR, exist_ok=True)
    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"vehicles.csv not found at {CSV_PATH}. Please run download_data.py first.")

    print(f"[1/6] Loading EPA vehicles dataset from {CSV_PATH}...")
    df = pd.read_csv(CSV_PATH, low_memory=False)
    print(f"Loaded {len(df):,} raw vehicle records.")

    # Data Cleaning
    print("[2/6] Cleaning data and removing target leakage...")
    # Keep only records where target comb08 is valid and > 0
    clean_df = df[df[TARGET].notna() & (df[TARGET] > 0)].copy()
    
    # Fill standard missing values for feature columns
    clean_df['displ'] = clean_df['displ'].fillna(0.0)
    clean_df['cylinders'] = clean_df['cylinders'].fillna(0)
    clean_df['drive'] = clean_df['drive'].fillna('Unknown')
    clean_df['trany'] = clean_df['trany'].fillna('Unknown')
    clean_df['fuelType1'] = clean_df['fuelType1'].fillna('Regular Gasoline')
    clean_df['VClass'] = clean_df['VClass'].fillna('Unknown')

    X = clean_df[ALL_FEATURES].copy()
    y = clean_df[TARGET].values

    print(f"Cleaned dataset: {len(clean_df):,} records with features: {ALL_FEATURES}")

    # Build Preprocessing Pipeline
    print("[3/6] Building Preprocessing Pipeline & Splitting Train/Test (80/20)...")
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, NUMERIC_FEATURES),
            ('cat', categorical_transformer, CATEGORICAL_FEATURES)
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42
    )
    print(f"Training set: {len(X_train):,} samples, Test set: {len(X_test):,} samples")

    # Model definition: Random Forest Regressor
    print("[4/6] Training Random Forest Regressor (n_estimators=100)...")
    rf_regressor = RandomForestRegressor(
        n_estimators=100,
        max_depth=22,
        min_samples_split=4,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )

    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', rf_regressor)
    ])

    pipeline.fit(X_train, y_train)
    print("[OK] Model training completed successfully.")

    # Evaluate on Test Set
    print("[5/6] Evaluating model performance on independent test set...")
    y_pred = pipeline.predict(X_test)
    mae = float(mean_absolute_error(y_test, y_pred))
    mse = float(mean_squared_error(y_test, y_pred))
    rmse = float(np.sqrt(mse))
    r2 = float(r2_score(y_test, y_pred))

    print(f"--- MODEL EVALUATION METRICS ---")
    print(f"Mean Absolute Error (MAE):     {mae:.2f} MPG")
    print(f"Root Mean Squared Error (RMSE): {rmse:.2f} MPG")
    print(f"R² (Coefficient of Determ.):   {r2:.4f}")

    # Feature Importances Extraction
    print("Calculating feature importances...")
    fitted_preprocessor = pipeline.named_steps['preprocessor']
    fitted_regressor = pipeline.named_steps['regressor']
    
    cat_feature_names = fitted_preprocessor.named_transformers_['cat'].named_steps['onehot'].get_feature_names_out(CATEGORICAL_FEATURES)
    all_feature_names = NUMERIC_FEATURES + list(cat_feature_names)
    raw_importances = fitted_regressor.feature_importances_

    # Calculate grouped importance by feature category
    grouped_importance = {
        'Engine Displacement (displ)': float(raw_importances[ALL_FEATURES.index('displ')]),
        'Engine Cylinders': float(raw_importances[ALL_FEATURES.index('cylinders')]),
        'Model Year': float(raw_importances[ALL_FEATURES.index('year')]),
        'Vehicle Class (VClass)': 0.0,
        'Transmission (trany)': 0.0,
        'Drive Type (drive)': 0.0,
        'Fuel Type (fuelType1)': 0.0
    }

    # Sum one-hot encoded importances into their original parent feature
    for name, imp in zip(cat_feature_names, raw_importances[len(NUMERIC_FEATURES):]):
        if name.startswith('VClass_'):
            grouped_importance['Vehicle Class (VClass)'] += float(imp)
        elif name.startswith('trany_'):
            grouped_importance['Transmission (trany)'] += float(imp)
        elif name.startswith('drive_'):
            grouped_importance['Drive Type (drive)'] += float(imp)
        elif name.startswith('fuelType1_'):
            grouped_importance['Fuel Type (fuelType1)'] += float(imp)

    # Convert to percentage and sort
    total_group_sum = sum(grouped_importance.values())
    feature_importance_list = [
        {"feature": k, "importance": round((v / total_group_sum) * 100, 2)}
        for k, v in sorted(grouped_importance.items(), key=lambda item: item[1], reverse=True)
    ]

    # Sample representative test points for Actual vs Predicted chart (spanning low to high MPG)
    test_indices = X_test.index
    eval_df = clean_df.loc[test_indices, ['year', 'make', 'model', TARGET]].copy()
    eval_df['actual_mpg'] = y_test
    eval_df['predicted_mpg'] = np.round(y_pred, 1)
    eval_df['error'] = np.round(np.abs(eval_df['actual_mpg'] - eval_df['predicted_mpg']), 2)
    
    # Pick 60 evenly spaced percentiles across sorted actual MPG for clean, non-cluttered chart
    eval_df_sorted = eval_df.sort_values(by='actual_mpg')
    sample_indices = np.linspace(0, len(eval_df_sorted) - 1, 60, dtype=int)
    sample_eval = eval_df_sorted.iloc[sample_indices]

    chart_points = []
    for idx, row in sample_eval.iterrows():
        chart_points.append({
            "vehicle": f"{int(row['year'])} {row['make']} {row['model']}",
            "actual_mpg": round(float(row['actual_mpg']), 1),
            "predicted_mpg": round(float(row['predicted_mpg']), 1),
            "actual_kmpl": round(float(row['actual_mpg']) * 0.425144, 2),
            "predicted_kmpl": round(float(row['predicted_mpg']) * 0.425144, 2),
            "error": round(float(row['error']), 1)
        })

    # Save Pipeline and Metrics
    print(f"[6/6] Saving pipeline to {PIPELINE_PATH}...")
    joblib.dump(pipeline, PIPELINE_PATH)
    print(f"[OK] Pipeline saved ({os.path.getsize(PIPELINE_PATH):,} bytes).")

    metrics_payload = {
        "algorithm": "Random Forest Regressor",
        "n_estimators": 100,
        "max_depth": 22,
        "total_records": len(clean_df),
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "metrics": {
            "mae": round(mae, 2),
            "rmse": round(rmse, 2),
            "r2_score": round(r2, 4)
        },
        "feature_importances": feature_importance_list,
        "actual_vs_predicted_samples": chart_points,
        "dataset_info": {
            "source": "U.S. EPA / FuelEconomy.gov",
            "year_min": int(clean_df['year'].min()),
            "year_max": int(clean_df['year'].max()),
            "total_makes": int(clean_df['make'].nunique()),
            "total_models": int(clean_df['model'].nunique())
        }
    }

    with open(METRICS_PATH, "w") as f:
        json.dump(metrics_payload, f, indent=2)
    print(f"[OK] Saved metrics and evaluation charts data to {METRICS_PATH}")

    # Build Fast SQLite Vehicle Catalog for Instant Frontend Dropdown Cascading
    print("\nBuilding SQLite vehicles catalog for high-speed dropdown queries...")
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE vehicles (
            id INTEGER PRIMARY KEY,
            year INTEGER,
            make TEXT,
            model TEXT,
            variant TEXT,
            displ REAL,
            cylinders REAL,
            trany TEXT,
            drive TEXT,
            fuelType1 TEXT,
            VClass TEXT,
            comb08 REAL
        )
    """)

    # Populate catalog
    clean_df['variant_str'] = clean_df.apply(format_variant_title, axis=1)
    
    rows = []
    for idx, row in clean_df.iterrows():
        rows.append((
            int(row['id']) if 'id' in row and pd.notna(row['id']) else int(idx),
            int(row['year']),
            str(row['make']).strip(),
            str(row['model']).strip(),
            str(row['variant_str']).strip(),
            float(row['displ']) if pd.notna(row['displ']) else 0.0,
            float(row['cylinders']) if pd.notna(row['cylinders']) else 0.0,
            str(row['trany']).strip() if pd.notna(row['trany']) else 'Unknown',
            str(row['drive']).strip() if pd.notna(row['drive']) else 'Unknown',
            str(row['fuelType1']).strip() if pd.notna(row['fuelType1']) else 'Regular Gasoline',
            str(row['VClass']).strip() if pd.notna(row['VClass']) else 'Unknown',
            float(row[TARGET])
        ))

    cursor.executemany("""
        INSERT INTO vehicles (id, year, make, model, variant, displ, cylinders, trany, drive, fuelType1, VClass, comb08)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, rows)

    # Create indexes for sub-millisecond query performance
    cursor.execute("CREATE INDEX idx_year ON vehicles (year)")
    cursor.execute("CREATE INDEX idx_year_make ON vehicles (year, make)")
    cursor.execute("CREATE INDEX idx_year_make_model ON vehicles (year, make, model)")
    conn.commit()
    conn.close()
    print(f"[OK] SQLite vehicles catalog successfully created at {DB_PATH} with {len(rows):,} vehicle records.")
    print("\nTraining and catalog pipeline complete!\n")

if __name__ == "__main__":
    train()
