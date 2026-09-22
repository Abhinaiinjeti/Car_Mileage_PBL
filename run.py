"""
AutoMileage AI - One-Command Application Launcher
Runs backend + frontend, verifies dataset and models, and opens your browser.
Usage:
    python run.py
"""

import os
import sys
import time
import webbrowser
import threading
import subprocess

# Ensure UTF-8 output if supported
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(BASE_DIR, "backend")
DATA_DIR = os.path.join(BACKEND_DIR, "data")
MODEL_DIR = os.path.join(BACKEND_DIR, "model")
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
CSV_PATH = os.path.join(DATA_DIR, "vehicles.csv")
MODEL_PATH = os.path.join(MODEL_DIR, "random_forest_pipeline.pkl")
DIST_INDEX = os.path.join(FRONTEND_DIR, "dist", "index.html")

PORT = 8000
HOST = "127.0.0.1"
URL = f"http://{HOST}:{PORT}"

def banner():
    print("=" * 68)
    print("   [AutoMileage AI] - Car Mileage Prediction Using Machine Learning")
    print("   B.Tech Project-Based Learning (PBL) System")
    print("=" * 68)

def ensure_dependencies():
    """Ensure data, model, and frontend bundle exist."""
    # 1. Check dataset
    if not os.path.exists(CSV_PATH) or os.path.getsize(CSV_PATH) < 1000000:
        print("[Launcher] Official EPA dataset not found. Downloading...")
        import backend.download_data as dd
        dd.download_and_extract_data()

    # 2. Check trained model
    if not os.path.exists(MODEL_PATH) or not os.path.exists(os.path.join(DATA_DIR, "vehicles_catalog.db")):
        print("[Launcher] Trained model or catalog not found. Training Random Forest...")
        import backend.train_model as tm
        tm.train()

    # 3. Check frontend build
    if not os.path.exists(DIST_INDEX):
        print("[Launcher] Built frontend not found. Compiling React app via npm build...")
        npm_cmd = "npm.cmd" if sys.platform == "win32" else "npm"
        subprocess.run([npm_cmd, "run", "build"], cwd=FRONTEND_DIR, check=True)

def open_browser():
    """Open browser after a brief delay to let uvicorn initialize."""
    time.sleep(1.8)
    print(f"\n[Launcher] Opening browser at {URL} ...")
    try:
        webbrowser.open(URL)
    except Exception as e:
        print(f"[Launcher] Could not open browser automatically: {e}")

def main():
    banner()
    print("[1/3] Verifying dataset, trained ML model, and frontend bundle...")
    ensure_dependencies()
    print("[2/3] All components verified successfully.")

    # Start browser launcher thread
    threading.Thread(target=open_browser, daemon=True).start()

    print(f"[3/3] Starting AutoMileage AI unified server on {URL} ...")
    print(f"      Press Ctrl+C to stop the application anytime.\n")
    print("-" * 68)

    import uvicorn
    # Run uvicorn server directly in process
    uvicorn.run("backend.main:app", host=HOST, port=PORT, log_level="info")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[Launcher] AutoMileage AI shut down cleanly. Goodbye!")
        sys.exit(0)
