# AutoMileage AI — Car Mileage Prediction Using Machine Learning

> **A B.Tech Project-Based Learning (PBL) Project**  
> Predicting real-world vehicle fuel efficiency without requiring users to input technical vehicle parameters.

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.3-61dafb.svg)](https://reactjs.org/)
[![Vite](https://img.shields.io/badge/Vite-5.4-purple.svg)](https://vitejs.dev/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.4+-orange.svg)](https://scikit-learn.org/)
[![Dataset](https://img.shields.io/badge/Dataset-U.S.%20EPA%20FuelEconomy-red.svg)](https://www.fueleconomy.gov)

---

## 1. Project Overview

**AutoMileage AI** is a full-stack, machine-learning-powered automotive web application designed to estimate vehicle fuel mileage ($km/L$ and $MPG$).

Unlike traditional or academic toy models that demand users to manually input technical engineering parameters (e.g., engine displacement in cubic centimeters, curb weight in kilograms, or horsepower), **AutoMileage AI** abstracts away technical complexity through an intuitive cascading selector:

$$\text{Select Year} \longrightarrow \text{Select Brand} \longrightarrow \text{Select Model} \longrightarrow \text{Select Variant} \longrightarrow \text{Predict Mileage}$$

The application automatically retrieves certified mechanical attributes from official U.S. EPA records and feeds them to a trained **Random Forest Regressor** to generate an immediate, genuine fuel economy prediction.

---

## 2. Problem Statement

Automobile fuel economy is a decisive factor for consumers, fleet managers, and environmental policy. However:
1. Most online mileage calculators require technical engineering metrics that everyday drivers do not know offhand.
2. Older academic projects rely heavily on the obsolete 1970s UCI Auto MPG dataset (398 cars, outdated carburetors, and manual inputs).
3. Many implementations introduce severe **target data leakage** (e.g., passing $CO_2$ emissions, fuel costs, or separate city/highway test cycles to predict combined mileage).

**AutoMileage AI** solves these issues by pairing an un-leaked Random Forest Regression pipeline trained on over 50,000 official EPA vehicle records with an accessible, consumer-grade automotive web interface.

---

## 3. Project Objectives

- **User-Centric Vehicle Selection:** Allow users to choose their vehicle by Year, Brand, Model, and Variant without manual spec entry.
- **Genuine Machine Learning:** Train a Random Forest Regressor on official U.S. EPA FuelEconomy data ($50,409$ vehicles from 1984 to 2027).
- **Strict Anti-Leakage Pipeline:** Train solely on intrinsic physical parameters (engine displacement, cylinders, transmission, drive axle, fuel type, vehicle class, and year).
- **Dual-Unit Results:** Report predictions primarily in kilometers per liter ($km/L$) alongside miles per gallon ($MPG$) using the exact constant:
  $$1\text{ MPG} = 0.425144\text{ km/L}$$
- **Full Transparency & Insights:** Present live model evaluation metrics ($MAE$, $RMSE$, $R^2$) and feature importances extracted directly from the trained model.

---

## 4. Technology Stack

### Frontend
- **React 18** (Modern component-driven UI)
- **Vite 5** (Ultra-fast build tool and dev server)
- **React Router 6** (Multi-page client routing: `/`, `/predict`, `/how-it-works`, `/about`)
- **Recharts** (Interactive data visualization for feature importance and actual vs. predicted curves)
- **Lucide React** (Clean, automotive iconography)
- **Native Modular CSS** (Crisp, classic automotive aesthetic without bulky CSS frameworks)

### Backend
- **Python 3.12**
- **FastAPI** (High-performance asynchronous REST API)
- **Pydantic v2** (Strict data validation and serialization)
- **SQLite3** (High-speed indexed catalog for sub-millisecond cascading dropdowns)

### Machine Learning
- **Scikit-Learn** (`RandomForestRegressor`, `ColumnTransformer`, `OneHotEncoder`, `StandardScaler`, `SimpleImputer`)
- **Pandas & NumPy** (Data cleaning and feature engineering)
- **Joblib** (Pipeline serialization and persistent caching)

---

## 5. Dataset Source & Features

- **Source:** Official [U.S. Environmental Protection Agency (EPA) / FuelEconomy.gov](https://www.fueleconomy.gov/feg/download.shtml) dataset (`vehicles.csv`).
- **Records:** $50,409$ real-world passenger and light commercial vehicles.
- **Model Years:** 1984 through 2027.
- **Target Variable:** `comb08` (Official EPA Combined City/Highway MPG for primary fuel).

### Features Used (Non-Leaked)
| Feature Name | Type | Description |
| :--- | :--- | :--- |
| `displ` | Numeric | Engine displacement in Liters (0.0 for pure EVs) |
| `cylinders` | Numeric | Number of engine cylinders (0 for pure EVs) |
| `year` | Numeric | Vehicle model year |
| `drive` | Categorical | Drive wheels (Front-Wheel, Rear-Wheel, All-Wheel, 4-Wheel Drive) |
| `trany` | Categorical | Transmission type and speed gearing |
| `fuelType1` | Categorical | Primary fuel type (Regular, Premium, Diesel, Electricity) |
| `VClass` | Categorical | EPA vehicle size classification (e.g., Midsize, SUV) |

---

## 6. Why Random Forest Regression?

1. **Non-Linear Relationships:** Internal combustion thermodynamics and aerodynamic drag are inherently non-linear; decision tree ensembles capture non-linear thresholds naturally.
2. **Tabular Robustness:** Excels on heterogeneous tabular datasets with both continuous and high-cardinality categorical attributes.
3. **Overfitting Resistance:** By training 100 decorrelated decision trees on bootstrap samples and averaging their outputs, variance is minimized compared to single decision trees.
4. **Interpretability:** Provides mathematically sound feature importance metrics derived from variance reduction (Gini impurity).
5. **Viva-Friendly:** Easy to illustrate and defend conceptually during academic evaluations.

---

## 7. Model Performance

Evaluated on an independent, unseen holdout test split ($20\%$, $10,082$ vehicles):

| Metric | Measured Value | Meaning |
| :--- | :--- | :--- |
| **MAE** | **$1.13$ MPG** ($0.48$ km/L) | Average deviation from certified EPA benchmark |
| **RMSE** | **$2.52$ MPG** ($1.07$ km/L) | Root Mean Squared Error penalizing larger errors |
| **$R^2$ Score** | **$0.9676$** | Explains $96.76\%$ of the variance in fuel consumption |

*Note: In regression, $R^2$ is the coefficient of determination, never to be called "accuracy".*

### Feature Importance Breakdown
1. **Engine Displacement:** $68.04\%$
2. **Engine Cylinders:** $22.97\%$
3. **Model Year:** $2.58\%$
4. **Vehicle Class:** $2.21\%$
5. **Transmission:** $1.75\%$
6. **Drive Type:** $1.48\%$
7. **Fuel Type:** $0.97\%$

---

## 8. Project Architecture & Structure

```text
Car_Mileage_PBL/
├── backend/
│   ├── data/
│   │   ├── download_data.py          # Auto-downloads & validates official EPA dataset
│   │   ├── vehicles.csv              # 50,409 raw EPA records
│   │   └── vehicles_catalog.db       # Indexed SQLite lookup catalog
│   ├── model/
│   │   ├── train_model.py            # Preprocessing + RF training + metrics exporter
│   │   ├── random_forest_pipeline.pkl# Serialized Scikit-learn pipeline
│   │   └── metrics.json              # Evaluated metrics, importances & test samples
│   ├── main.py                       # FastAPI application & REST endpoints
│   └── requirements.txt              # Backend dependencies
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx            # Responsive header with mobile hamburger menu
│   │   │   └── Footer.jsx            # Clean footer with academic credits & disclaimers
│   │   ├── pages/
│   │   │   ├── Home.jsx              # Landing page (Hero, 3 feature cards, flow, disclaimer)
│   │   │   ├── Predict.jsx           # Cascading Year->Make->Model->Variant & Result card
│   │   │   ├── HowItWorks.jsx        # 5-step breakdown, tree diagram & Why RF
│   │   │   └── About.jsx             # Project info, dataset facts, Recharts graphs
│   │   ├── services/
│   │   │   └── api.js                # Frontend API client
│   │   ├── styles/
│   │   │   └── index.css             # Automotive styling system
│   │   ├── App.jsx                   # React Router setup
│   │   └── main.jsx                  # React DOM root
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
│
├── README.md                         # Project documentation
├── PROJECT_DOCUMENTATION.md          # 24-section B.Tech PBL report
└── .gitignore
```

---

## 9. Installation & Execution Guide

### Quick Start: Run Everything With One Command!

Simply run:
```bash
python run.py
```
*(Or double-click `run.bat` on Windows)*

**What this one command does automatically:**
1. Verifies that the official EPA dataset is present (downloads it if missing).
2. Verifies that the Random Forest model and SQLite catalog exist (trains it if missing).
3. Verifies that the React production bundle is built (compiles via npm if missing).
4. Launches the unified FastAPI server on `http://127.0.0.1:8000`.
5. Automatically opens your default web browser to the application!

---

### Prerequisites (for manual setup)
- **Python 3.10+** (Tested on Python 3.12)
- **Node.js 18+** & **npm**

### Manual Step-by-Step Setup (Optional)

---

## 10. API Endpoints Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/health` | Service health status and model availability |
| `GET` | `/api/years` | Returns distinct model years (descending) |
| `GET` | `/api/makes?year={year}` | Returns brands available for selected year |
| `GET` | `/api/models?year={year}&make={make}` | Returns models for selected year and brand |
| `GET` | `/api/variants?year={year}&make={make}&model={model}` | Returns valid trim/engine configurations |
| `POST` | `/api/predict` | Predicts mileage ($MPG$ and $km/L$) for vehicle configuration |
| `GET` | `/api/model-insights` | Returns calculated $MAE$, $RMSE$, $R^2$, and chart points |

---

## 11. Limitations & Future Scope

### Limitations
- The model is trained on U.S. EPA certification test cycles; driving in severe traffic or extreme weather can cause discrepancies.
- Regional models exclusive to Asian or European domestic markets (that were never certified by the EPA) are not in the EPA database.

### Future Scope
- Integration with OBD-II telematics data for real-time telemetry-based fine-tuning.
- Support for personalized driving profile adjustments (city vs. highway percentage slider).
- Fuel cost estimator based on regional fuel prices.

---

## 12. Academic Citation & Credits

- **Student PBL Project:** AutoMileage AI
- **Dataset Courtesy:** [United States Environmental Protection Agency & U.S. Department of Energy (FuelEconomy.gov)](https://www.fueleconomy.gov)
- **Algorithm:** Random Forest Regression via Scikit-Learn

© 2026 AutoMileage AI.
