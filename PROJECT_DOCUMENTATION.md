# AutoMileage AI — Car Mileage Prediction Using Machine Learning
## B.Tech Project-Based Learning (PBL) Comprehensive Project Documentation

---

## Table of Contents
1. [Abstract](#1-abstract)
2. [Introduction](#2-introduction)
3. [Problem Statement](#3-problem-statement)
4. [Existing System](#4-existing-system)
5. [Proposed System](#5-proposed-system)
6. [Objectives](#6-objectives)
7. [Scope](#7-scope)
8. [Dataset](#8-dataset)
9. [Dataset Source](#9-dataset-source)
10. [Feature Description](#10-feature-description)
11. [Data Preprocessing](#11-data-preprocessing)
12. [Random Forest Regression](#12-random-forest-regression)
13. [System Architecture](#13-system-architecture)
14. [Frontend](#14-frontend)
15. [Backend](#15-backend)
16. [API](#16-api)
17. [Implementation](#17-implementation)
18. [Model Evaluation](#18-model-evaluation)
19. [Results](#19-results)
20. [Advantages](#20-advantages)
21. [Limitations](#21-limitations)
22. [Future Scope](#22-future-scope)
23. [Conclusion](#23-conclusion)
24. [References](#24-references)

---

## 1. Abstract

Fuel efficiency remains one of the primary criteria considered by consumers and automotive professionals when evaluating motor vehicles. Traditional automated mileage predictors and academic machine-learning projects often suffer from significant practical hurdles: they demand that end users manually input esoteric technical vehicle attributes (e.g., displacement in cubic centimeters, curb weight in kilograms, or engine horsepower), rely on obsolete datasets (such as the 1970s UCI Auto MPG dataset), or inadvertently introduce target leakage by using derived emissions ratings to predict mileage. 

This project, **AutoMileage AI**, presents an end-to-end Machine Learning web application designed to solve these issues. By leveraging an official repository of over $50,000$ real-world certified vehicles from the United States Environmental Protection Agency (EPA) / FuelEconomy.gov spanning 1984 through 2027, the application enables consumers to estimate vehicle fuel efficiency simply by selecting their vehicle’s Year, Brand, Model, and Variant. The system automatically retrieves verified mechanical attributes from an indexed catalog and routes them through a trained **Random Forest Regression** pipeline. On an unseen test set of $10,082$ vehicles, the model achieved a Mean Absolute Error ($MAE$) of $1.13\text{ MPG}$, a Root Mean Squared Error ($RMSE$) of $2.52\text{ MPG}$, and an $R^2$ score of $0.9676$. Results are converted seamlessly into consumer-friendly kilometers per liter ($km/L$), bridging practical usability with machine-learning accuracy.

---

## 2. Introduction

Vehicle fuel economy is governed by complex mechanical, aerodynamic, and thermodynamic interactions involving engine displacement, cylinder layout, transmission gearing, vehicle weight class, and drive configuration. Predicting fuel economy reliably through computational models enables consumers to make informed purchasing choices, understand operating expenses, and evaluate the environmental impact of their transportation.

In undergraduate engineering and project-based learning curricula, machine-learning regression is frequently demonstrated on toy datasets. However, real-world engineering requires addressing the complete lifecycle: obtaining raw public certification data, cleaning and pre-processing heterogeneous tabular records, eliminating target data leakage, training robust ensemble models, deploying an asynchronous backend server, and designing an accessible, responsive web interface.

**AutoMileage AI** was developed as a B.Tech Project-Based Learning initiative to demonstrate this complete engineering cycle. The application provides an interface that mirrors commercial automotive portals (e.g., Edmunds, Kelley Blue Book, or AutoTrader) while maintaining technical fidelity and statistical rigor.

---

## 3. Problem Statement

Estimating automobile fuel economy using modern predictive modeling poses three major challenges:
1. **User Accessibility Barrier:** Ordinary car owners, prospective buyers, and college evaluators do not know their vehicle’s exact displacement in cubic inches, transmission gear ratios, or curb weight off the top of their heads. Requiring manual entry of these metrics causes user drop-off or incorrect predictions due to faulty inputs.
2. **Dataset Irrelevance in Academic Projects:** A substantial number of machine learning projects continue to train on the legacy 1983 UCI Auto MPG dataset (which comprises only 398 vehicles with 3-speed automatic transmissions and carburetors from the 1970s). Such models fail completely when applied to contemporary automobiles featuring 8-speed automatic transmissions, multi-point variable valve timing, turbocharging, and hybrid drivetrains.
3. **Data Leakage in Modeling:** Many public machine-learning notebooks inadvertently train models on features such as city fuel economy ($city08$), highway fuel economy ($highway08$), annual fuel cost ($fuelCost08$), or $CO_2$ greenhouse gas tailpipe emissions ($co2TailpipeGpm$) to predict combined fuel economy ($comb08$). Because these features are direct mathematical derivatives or linear combinations of the target, the reported model accuracy is artificially inflated and useless for real prediction.

---

## 4. Existing System

Traditional systems for fuel mileage estimation generally fall into two categories:

1. **Static Catalog Lookups:** Traditional automotive websites store flat fuel-economy ratings. While accurate for existing cataloged vehicles, they offer no algorithmic understanding, cannot evaluate non-standard trims or hypothetical configurations, and do not model feature interactions.
2. **Academic Manual-Entry Forms:** Typical academic ML projects present a form requiring the user to type numerical values into 7 to 10 input fields (e.g., horsepower, displacement, cylinders, vehicle weight, acceleration in seconds). 
   - *Drawbacks:* Error-prone user input, lack of cascading validation, disjointed user experience, and poor aesthetic design.

---

## 5. Proposed System

**AutoMileage AI** bridges the gap between catalog usability and predictive machine learning:

1. **Dynamic 4-Step Cascading Selection:** The user interacts only with four intuitive dropdown menus:
   $$\text{Select Model Year} \longrightarrow \text{Select Make/Brand} \longrightarrow \text{Select Model} \longrightarrow \text{Select Variant}$$
2. **Automated Feature Retrieval:** Upon variant selection, the backend service fetches verified intrinsic mechanical attributes (displacement, cylinder count, transmission type, drivetrain, fuel type, vehicle class) from an indexed SQLite catalog.
3. **Leakage-Free Random Forest Regression:** The extracted feature vector is fed into a trained Scikit-Learn Random Forest Regressor pipeline that computes the estimated fuel consumption.
4. **Dual-Unit Consumer Presentation:** The application displays the estimated mileage prominently in kilometers per liter ($km/L$) as well as miles per gallon ($MPG$), accompanied by an intuitive efficiency badge and a breakdown of the vehicle’s mechanical specifications.
5. **Interactive Model Insights:** The platform provides a dedicated About & Insights dashboard displaying live performance metrics ($MAE$, $RMSE$, $R^2$), horizontal feature importance bars, and holdout test set actual-versus-predicted plots rendered via Recharts.

---

## 6. Objectives

- Design and deploy an end-to-end full-stack machine learning web application.
- Automate data ingestion from official government repositories ([FuelEconomy.gov](https://www.fueleconomy.gov)).
- Enforce strict target leakage elimination during feature selection.
- Implement a robust data preprocessing and encoding pipeline using Scikit-Learn `ColumnTransformer`.
- Train and hyperparameter-tune a 100-tree Random Forest Regressor.
- Deliver sub-millisecond cascading dropdown queries using an indexed relational catalog.
- Develop a responsive React frontend adhering to classic, professional automotive design standards.
- Provide comprehensive model transparency and evaluation metrics for academic evaluation.

---

## 7. Scope

- **In-Scope:**
  - Certified passenger automobiles, light-duty trucks, minivans, and SUVs from model year 1984 through 2027.
  - Internal combustion engines (Gasoline, Diesel) and Hybrid/Electric powertrains certified under U.S. EPA test cycles.
  - Web deployment on desktop, tablet, and mobile browsers with responsive navigation.
  - Asynchronous RESTful API communication between FastAPI backend and React frontend.
- **Out-of-Scope:**
  - Heavy commercial vehicles (Class 7 and 8 freight trucks, construction machinery).
  - Uncertified grey-market vehicles lacking standardized regulatory cycle testing.
  - Real-time GPS/telematics tracking of instant throttle position or tire pressure.

---

## 8. Dataset

The project utilizes the comprehensive, official vehicle certification dataset provided by the **United States Environmental Protection Agency (EPA)** and the **U.S. Department of Energy (DOE)**.

### Dataset Overview
- **Raw File Name:** `vehicles.csv` (extracted from `vehicles.csv.zip`)
- **Total Records:** $50,409$ vehicle configurations
- **Total Attributes:** $84$ regulatory and technical columns
- **Time Span:** Model years $1984$ through $2027$
- **Total Automotive Manufacturers:** $146$ unique makes (including Toyota, Ford, Honda, BMW, Mercedes-Benz, Chevrolet, Audi, Porsche, Nissan, Hyundai, etc.)
- **Target Missing Rate:** $0.0\%$ (all records have certified $comb08$ ratings)

---

## 9. Dataset Source

The dataset was fetched directly from the official public repository maintained by the U.S. government:
- **Hosting Portal:** [FuelEconomy.gov Data Downloads](https://www.fueleconomy.gov/feg/download.shtml)
- **Direct Zip Archive:** `https://www.fueleconomy.gov/feg/epadata/vehicles.csv.zip`
- **Citation:** U.S. Department of Energy & U.S. Environmental Protection Agency, *Fuel Economy Guide and Certification Data*, public domain government dataset.

---

## 10. Feature Description

To ensure strict prevention of target data leakage, all features that directly derive from or correlate mathematically with fuel consumption test cycles were purged.

### Selected Input Features
1. **`displ` (Engine Displacement):** Numerical (float). Total volume of all engine cylinders expressed in Liters (e.g., $2.0$, $3.5$, $5.0$). Pure electric vehicles have a displacement of $0.0\text{ L}$.
2. **`cylinders` (Engine Cylinders):** Numerical (float/integer). Number of engine combustion chambers (e.g., $4$, $6$, $8$, $12$). Pure electric vehicles have $0$ cylinders.
3. **`year` (Model Year):** Numerical (integer). Calendar year of vehicle manufacture ($1984$ to $2027$).
4. **`drive` (Drive Axle Configuration):** Categorical. Mechanism transmitting engine torque to wheels:
   - Front-Wheel Drive (FWD)
   - Rear-Wheel Drive (RWD)
   - All-Wheel Drive (AWD)
   - 4-Wheel Drive (4WD)
   - 2-Wheel Drive
5. **`trany` (Transmission Type & Speeds):** Categorical. Transmission gearing mechanism (e.g., Automatic 8-spd, Manual 6-spd, Automatic (AV-S6), Continuously Variable Transmission).
6. **`fuelType1` (Primary Fuel Type):** Categorical. Chemical source of energy (e.g., Regular Gasoline, Premium Gasoline, Diesel, Electricity).
7. **`VClass` (Vehicle Class Category):** Categorical. EPA physical vehicle footprint and interior volume classification (e.g., Compact Cars, Midsize Cars, Large Cars, Small Sport Utility Vehicle 4WD, Standard Pickup Trucks).

### Target Variable
- **`comb08` (Combined Fuel Economy):** Numerical (float). Official EPA combined city/highway fuel economy in Miles Per Gallon ($MPG$). Calculated according to the EPA 55% city / 45% highway weighting formula.

---

## 11. Data Preprocessing

Data preprocessing is encapsulated in a reproducible Scikit-Learn `ColumnTransformer` pipeline:

```
                      ┌───────────────────────────────────────────────┐
                      │                 Raw Features                  │
                      └──────────────────────┬────────────────────────┘
                                             │
                     ┌───────────────────────┴───────────────────────┐
                     ▼                                               ▼
         [Numeric Features]                              [Categorical Features]
         (year, displ, cylinders)                        (drive, trany, fuelType1, VClass)
                     │                                               │
                     ▼                                               ▼
         SimpleImputer(strategy='median')                SimpleImputer(strategy='most_frequent')
                     │                                               │
                     ▼                                               ▼
         StandardScaler()                                OneHotEncoder(handle_unknown='ignore')
                     │                                               │
                     └───────────────────────┬───────────────────────┘
                                             │
                                             ▼
                               Feature Matrix (40,327 x N)
                                             │
                                             ▼
                               Random Forest Regressor (100 Trees)
```

1. **Handling Missing Values:**
   - Numerical attributes (`displ`, `cylinders`) with missing entries are imputed using the **median** value of the column.
   - Categorical attributes with missing entries are imputed using the **most frequent** category.
2. **Feature Scaling:**
   - Numerical attributes undergo Z-score standard scaling ($\mu = 0, \sigma = 1$).
3. **Categorical Encoding:**
   - High-cardinality and nominal features are encoded via `OneHotEncoder(handle_unknown='ignore', sparse_output=False)`. Unseen categories during inference gracefully evaluate to zero-vectors without throwing runtime exceptions.
4. **Data Splitting:**
   - The preprocessed dataset is partitioned into an **80% training set** ($40,327$ records) and a **20% holdout test set** ($10,082$ records) using a fixed random seed (`random_state=42`).

---

## 12. Random Forest Regression

### Algorithm Principles
Random Forest is an ensemble learning method based on the principle of **Bootstrap Aggregation (Bagging)**:
1. $B = 100$ distinct decision trees are constructed.
2. Each individual tree $T_b$ is trained on a distinct bootstrap sample drawn with replacement from the training dataset.
3. At each decision node in every tree, only a random subset of features $m \approx \sqrt{p}$ is considered for splitting, decorrelating the individual trees.
4. For regression, the ensemble prediction $\hat{y}$ for input vector $x$ is the unweighted arithmetic mean of all $B$ individual tree predictions:
   $$\hat{y}(x) = \frac{1}{B} \sum_{b=1}^{B} T_b(x)$$

### Hyperparameter Specifications
- `n_estimators`: $100$ trees
- `max_depth`: $22$
- `min_samples_split`: $4$
- `min_samples_leaf`: $2$
- `random_state`: $42$
- `n_jobs`: $-1$ (utilizes all CPU cores in parallel)

### Justification for Project-Based Learning
- **Non-Linear Dynamics:** Internal combustion thermal efficiency and vehicle drag coefficients follow non-linear curves that linear regression cannot fit.
- **Heterogeneous Attributes:** Random Forest handles mixtures of continuous metrics and discrete categorical labels without requiring artificial normalization assumptions.
- **Robustness:** Averaging 100 trees cancels out variance, preventing severe prediction spikes on unusual vehicle configurations.

---

## 13. System Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│                          CLIENT BROWSER                                │
│                                                                        │
│   React 18 + Vite SPA  (React Router: /, /predict, /how-it-works, /about)│
│   Recharts Visualizations  •  Responsive Mobile/Desktop UI             │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                HTTP JSON (REST)
                                    │
┌───────────────────────────────────▼────────────────────────────────────┐
│                       FASTAPI BACKEND SERVER                           │
│                                                                        │
│   • CORS Middleware                                                    │
│   • Input Validation (Pydantic v2)                                     │
│   • Cascading Metadata Endpoints (/api/years, /makes, /models, /var)   │
│   • Prediction Engine (/api/predict)                                   │
│   • Model Insights Service (/api/model-insights)                       │
└──────────────────┬─────────────────────────────────┬───────────────────┘
                   │                                 │
                   ▼                                 ▼
   ┌───────────────────────────────┐ ┌──────────────────────────────────┐
   │    SQLite Vehicle Catalog     │ │    Trained ML Pipeline (Joblib)  │
   │  (50,409 Indexed Vehicles)    │ │   (ColumnTransformer + RF Reg)   │
   └───────────────────────────────┘ └──────────────────────────────────┘
```

---

## 14. Frontend

The frontend is constructed using **React 18** and bundled with **Vite 5**.

### Key Components & Pages
1. **`Navbar.jsx`:** Clean header featuring the AutoMileage AI brand, desktop navigation links, and a responsive SVG hamburger menu toggle for mobile viewports.
2. **`Footer.jsx`:** Universal footer displaying B.Tech PBL attribution, academic disclaimer, navigation links, and official EPA source citations.
3. **`Home.jsx` (`/`):**
   - Hero banner with headline *"Know Your Car's Mileage"* and call-to-action buttons.
   - Clean automotive vector illustration SVG.
   - Three feature highlights: **Simple** (no manual spec entry), **Smart** (ML analyzed), and **Quick** (instant estimate).
   - Step-by-step visual process flow and disclaimer.
4. **`Predict.jsx` (`/predict`):**
   - Centered card with 4 dynamically cascading dropdown menus.
   - Progressive disclosure: each dropdown activates only after the preceding selection is made.
   - Primary button: *"🚗 Predict My Mileage"* (disabled until valid selection, shows loading spinner during computation).
   - Large result card with primary $km/L$ typography, secondary $MPG$ conversion, efficiency rating badge, and vehicle specs grid.
5. **`HowItWorks.jsx` (`/how-it-works`):**
   - 5-step user walkthrough explaining how vehicle selection translates to dataset specifications, decision tree ensembles, and conversion formulas.
   - Formatted ASCII decision tree ensemble diagram.
   - Academic explanation section: *"Why Random Forest?"*.
6. **`About.jsx` (`/about`):**
   - Project background and academic purpose.
   - Official EPA dataset specifications table.
   - Live performance metric cards ($MAE$, $RMSE$, $R^2$).
   - Interactive horizontal feature importance bar chart via Recharts.
   - Actual vs. Predicted comparison chart via Recharts across holdout test vehicles.

---

## 15. Backend

The backend is developed with **FastAPI** running on top of the **Uvicorn** ASGI server.

### Key Architectural Strengths
- **Sub-Millisecond Metadata Retrieval:** An indexed SQLite relational database stores all vehicle configurations with B-Tree indexes on `(year, make, model)`, eliminating runtime dataset scanning.
- **Model In-Memory Persistence:** The trained Scikit-Learn pipeline is loaded into memory on server startup via Joblib, allowing predictions to execute in under $5\text{ milliseconds}$.
- **Strict Pydantic Validation:** All client request payloads are validated and typed before hitting business logic.
- **Dual-Unit Conversion Engine:** Internally evaluates fuel economy and executes standard conversion:
  $$\text{Mileage}_{\text{km/L}} = \text{Mileage}_{\text{MPG}} \times 0.425144$$

---

## 16. API

The RESTful API provides the following endpoints:

| Endpoint | Method | Query / Payload | Response Description |
| :--- | :--- | :--- | :--- |
| `/api/health` | `GET` | None | Confirms backend service health and model status |
| `/api/years` | `GET` | None | Returns sorted list of distinct vehicle model years |
| `/api/makes` | `GET` | `year=2024` | Returns all automotive brands available for the given year |
| `/api/models` | `GET` | `year=2024&make=Toyota` | Returns all car models available for the selected year and make |
| `/api/variants` | `GET` | `year=2024&make=Toyota&model=Camry` | Returns valid powertrain and trim configurations with vehicle IDs |
| `/api/predict` | `POST` | `{"vehicle_id": 47085}` | Executes ML pipeline and returns predicted $km/L$, $MPG$, and specs |
| `/api/model-insights` | `GET` | None | Returns test-set $MAE$, $RMSE$, $R^2$, and sample plot coordinates |

### Example Prediction Request & Response
**Request:**
```http
POST /api/predict HTTP/1.1
Content-Type: application/json

{
  "vehicle_id": 47085
}
```

**Response:**
```json
{
  "vehicle": "2024 Toyota Camry",
  "variant": "6 Cyl | 3.5L | Automatic (S8) | Front-Wheel Drive",
  "year": 2024,
  "make": "Toyota",
  "model": "Camry",
  "predicted_mpg": 25.5,
  "predicted_kmpl": 10.8,
  "efficiency_rating": "Moderate Efficiency",
  "specs": {
    "engine": "3.5 L",
    "cylinders": "6 Cylinders",
    "transmission": "Automatic (S8)",
    "fuel_type": "Regular Gasoline",
    "drive_type": "Front-Wheel Drive",
    "vehicle_class": "Midsize Cars"
  },
  "conversion_standard": "1 MPG = 0.425144 km/L"
}
```

---

## 17. Implementation

### Execution Pipeline
1. **`download_data.py`:** Fetches `https://www.fueleconomy.gov/feg/epadata/vehicles.csv.zip`, extracts `vehicles.csv` into `backend/data/`, and validates file integrity.
2. **`train_model.py`:**
   - Filters records with valid $comb08$ targets.
   - Cleans missing numerical and categorical values.
   - Configures `ColumnTransformer` with `StandardScaler` and `OneHotEncoder`.
   - Fits `RandomForestRegressor(n_estimators=100, max_depth=22, random_state=42)`.
   - Evaluates predictions on the unseen 20% test partition.
   - Serializes the trained pipeline into `backend/model/random_forest_pipeline.pkl`.
   - Exports evaluation metrics, feature importances, and sample coordinates to `backend/model/metrics.json`.
   - Constructs the relational SQLite table `vehicles` with multi-column indexes in `backend/data/vehicles_catalog.db`.
3. **`main.py`:** Boots the FastAPI service and mounts REST routes.
4. **Vite + React:** Serves the frontend bundle with automatic reverse proxy routing for API calls.

---

## 18. Model Evaluation

The model was evaluated against the unseen holdout test partition comprising **$10,082$ real vehicle records**.

### Evaluation Equations
1. **Mean Absolute Error (MAE):**
   $$\text{MAE} = \frac{1}{N} \sum_{i=1}^{N} \left| y_i - \hat{y}_i \right|$$
2. **Root Mean Squared Error (RMSE):**
   $$\text{RMSE} = \sqrt{\frac{1}{N} \sum_{i=1}^{N} (y_i - \hat{y}_i)^2}$$
3. **Coefficient of Determination ($R^2$):**
   $$R^2 = 1 - \frac{\sum_{i=1}^{N} (y_i - \hat{y}_i)^2}{\sum_{i=1}^{N} (y_i - \bar{y})^2}$$

### Evaluated Test Metrics
| Metric | Value |
| :--- | :--- |
| **Mean Absolute Error (MAE)** | **$1.13\text{ MPG}$** ($0.48\text{ km/L}$) |
| **Root Mean Squared Error (RMSE)** | **$2.52\text{ MPG}$** ($1.07\text{ km/L}$) |
| **$R^2$ Score** | **$0.9676$** |

*Academic Note:* The $R^2$ score indicates that $96.76\%$ of the total variance in vehicle fuel economy is explained by the model’s selected physical parameters without introducing any target leakage.

---

## 19. Results

### Feature Importance Hierarchy
Analysis of impurity reduction across all 100 decision trees reveals the following relative feature importance hierarchy:

| Feature Category | Relative Importance (%) | Physical Rationale |
| :--- | :--- | :--- |
| **Engine Displacement (`displ`)** | **$68.04\%$** | Primary determinant of air-fuel charge volume per engine cycle. |
| **Engine Cylinders (`cylinders`)** | **$22.97\%$** | Frictional surface area and volumetric thermal losses. |
| **Model Year (`year`)** | **$2.58\%$** | Technological advancements in engine efficiency and aerodynamics. |
| **Vehicle Class (`VClass`)** | **$2.21\%$** | Frontal surface area, weight category, and aerodynamic drag. |
| **Transmission (`trany`)** | **$1.75\%$** | Gear spread, torque converter lockup, and transmission parasitic loss. |
| **Drive Type (`drive`)** | **$1.48\%$** | Driveline friction and rotational inertia (AWD/4WD vs. FWD). |
| **Fuel Type (`fuelType1`)** | **$0.97\%$** | Energy density per gallon (Diesel vs. Regular Gasoline vs. Electricity). |

---

## 20. Advantages

- **Zero Manual Technical Spec Entry:** Normal consumers never need to guess engine displacement, transmission gear counts, or vehicle weights.
- **Genuine Machine Learning:** Predictions are computed directly by an active Random Forest model rather than displaying static database entries.
- **No Data Leakage:** Features are strictly constrained to intrinsic vehicle properties.
- **Real-World Scale:** Trained on $50,409$ vehicles covering over $40$ years of automotive history.
- **Sub-Millisecond Response:** SQLite B-Tree indexing guarantees instantaneous dropdown transitions.
- **Dual Unit Display:** Displays primary results in $km/L$ alongside official $MPG$ values.
- **Educational Transparency:** Live performance metrics, feature importances, and interactive Recharts graphs support peer review and academic viva evaluations.

---

## 21. Limitations

1. **Test-Cycle Idealization:** Predictions reflect standardized EPA dynamometer test cycles. Aggressive acceleration, heavy cargo, mountainous terrain, extreme weather, or sub-optimal tire pressures can lead to divergence in real-world driving.
2. **Regional Coverage Scope:** The underlying dataset covers vehicles certified for sale in the United States market. Select domestic vehicles sold exclusively in international markets (e.g., specific domestic Japanese Kei cars or Indian market models) are not present in the EPA database.
3. **Static Driving Profile:** The model predicts a standard 55% city / 45% highway combined profile and does not yet allow interactive adjustment of personalized driving splits.

---

## 22. Future Scope

- **Driver Behavior Parameterization:** Incorporate an interactive driving profile slider allowing users to adjust their personal city vs. highway driving ratio.
- **OBD-II Telematics Integration:** Interface with live vehicle telematics dongles to calibrate predictions against individual driving habits and throttle response.
- **Fuel Cost & Environmental Impact Calculator:** Integrate real-time localized fuel price APIs to compute expected annual fuel expenditures and $CO_2$ footprint.
- **Hybrid Battery Health Factor:** Add battery degradation adjustment factors for older hybrid and plug-in electric vehicles.

---

## 23. Conclusion

The **AutoMileage AI** project successfully demonstrates the design, training, and deployment of a modern Machine Learning application for vehicle fuel economy prediction. By replacing manual technical inputs with an intuitive, dynamic 4-step cascading selector backed by an indexed catalog of official EPA vehicle data, the application achieves a consumer-grade user experience while maintaining statistical integrity.

The Random Forest Regression pipeline delivers high predictive accuracy ($MAE = 1.13\text{ MPG}$, $R^2 = 0.9676$) without target leakage, validating that intrinsic mechanical attributes—chiefly engine displacement and cylinder layout—strongly govern fuel efficiency. AutoMileage AI provides an accessible platform for consumers and a comprehensive demonstration of applied Machine Learning for academic engineering evaluations.

---

## 24. References

1. **U.S. Environmental Protection Agency & U.S. Department of Energy:** *Fuel Economy Guide and Data Files (1984–2027)*, [fueleconomy.gov](https://www.fueleconomy.gov).
2. **Breiman, Leo:** *Random Forests*, Machine Learning, Vol. 45, No. 1, pp. 5–32, 2001.
3. **Pedregosa, F. et al.:** *Scikit-learn: Machine Learning in Python*, Journal of Machine Learning Research, Vol. 12, pp. 2825–2830, 2011.
4. **Tiangolo, Sebastián:** *FastAPI — Modern, High-Performance Web Framework for Python*, [fastapi.tiangolo.com](https://fastapi.tiangolo.com).
5. **Facebook Open Source:** *React: A JavaScript Library for Building User Interfaces*, [react.dev](https://react.dev).
6. **Heydon Pickering:** *Inclusive Design Patterns: Coding Accessibility Into Web Applications*, Smashing Magazine, 2016.

---
*AutoMileage AI — B.Tech Project-Based Learning © 2026*
