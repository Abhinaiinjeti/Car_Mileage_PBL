#!/usr/bin/env bash
# Exit immediately if a command exits with a non-zero status
set -o errexit

echo "=================================================="
echo "   AutoMileage AI - Render Cloud Build Script     "
echo "=================================================="

echo "[1/4] Installing Python dependencies..."
pip install --upgrade pip
pip install -r backend/requirements.txt

echo "[2/4] Building React Frontend with Vite..."
cd frontend
npm install
npm run build
cd ..

echo "[3/4] Downloading official EPA FuelEconomy dataset..."
python backend/download_data.py

echo "[4/4] Training Random Forest model & creating indexed catalog..."
python backend/train_model.py

echo "=================================================="
echo "   Build Succeeded! Ready for deployment.        "
echo "=================================================="
