"""
AutoMileage AI - Data Downloader
Downloads official U.S. EPA / FuelEconomy.gov vehicle data.
Source: https://www.fueleconomy.gov/feg/download.shtml
"""

import os
import sys
import zipfile
import urllib.request
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
ZIP_URL = "https://www.fueleconomy.gov/feg/epadata/vehicles.csv.zip"
ZIP_PATH = os.path.join(DATA_DIR, "vehicles.csv.zip")
CSV_PATH = os.path.join(DATA_DIR, "vehicles.csv")

def download_and_extract_data():
    os.makedirs(DATA_DIR, exist_ok=True)

    if os.path.exists(CSV_PATH) and os.path.getsize(CSV_PATH) > 1000000:
        print(f"[OK] Dataset already exists at: {CSV_PATH} ({os.path.getsize(CSV_PATH):,} bytes)")
    else:
        print(f"[1/3] Downloading official EPA FuelEconomy dataset from:\n  {ZIP_URL}")
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AutoMileageAI/1.0"}
        req = urllib.request.Request(ZIP_URL, headers=headers)
        
        with urllib.request.urlopen(req, timeout=60) as response, open(ZIP_PATH, 'wb') as out_file:
            data = response.read()
            out_file.write(data)
        print(f"[2/3] Downloaded zip archive ({os.path.getsize(ZIP_PATH):,} bytes).")

        print("[3/3] Extracting vehicles.csv...")
        with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
            zip_ref.extractall(DATA_DIR)
        print(f"[OK] Extracted to {CSV_PATH} ({os.path.getsize(CSV_PATH):,} bytes)")

    # Validate dataset
    df = pd.read_csv(CSV_PATH, low_memory=False)
    print(f"\n--- EPA FuelEconomy Dataset Validation ---")
    print(f"Total vehicle records: {len(df):,}")
    print(f"Total columns: {len(df.columns)}")
    print(f"Year range: {df['year'].min()} - {df['year'].max()}")
    print(f"Total unique makes: {df['make'].nunique()}")
    print(f"Sample columns of interest: make, model, year, displ, cylinders, trany, drive, fuelType1, comb08")
    
    missing_comb = df['comb08'].isna().sum()
    print(f"Missing combined MPG (comb08): {missing_comb}")
    print("Dataset verification complete!\n")
    return CSV_PATH

if __name__ == "__main__":
    download_and_extract_data()
