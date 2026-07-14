# Swarovski Pearl Yield Prediction

## Overview

This project develops an end-to-end machine learning pipeline for predicting manufacturing yield (**Okper**) in Swarovski pearl production.

The notebook follows a production-oriented workflow covering data preprocessing, exploratory data analysis, feature engineering, feature selection, model development, hyperparameter optimization, explainability, and generation of deployment-ready artifacts.

The objective is to identify the key factors affecting manufacturing yield while building a robust and reproducible prediction pipeline for future production batches.

---

## Problem Statement

Manufacturing yield directly impacts production efficiency, material utilization, and overall manufacturing cost. Predicting yield before production completion enables better planning, process optimization, and early identification of quality issues.

This project builds regression models to predict the percentage of acceptable pearls (**Okper**) using historical production batches, product information, colour attributes, manufacturing defects, and process-related variables.

The final pipeline emphasizes reproducibility, leakage-aware feature engineering, and model interpretability suitable for industrial applications.

---

## Dataset

The dataset used in this project is **proprietary** and cannot be shared publicly.

It contains:

- Manufacturing batch information
- Product and colour codes
- Defect counts across multiple stages
- Yield percentage (Okper)

### Data Access

To run this project, place the dataset files inside the `data/` folder:

```bash
data/
│
├── cp_results.csv
├── colour_code.csv
├── product_code.csv
└── dictionary.csv
```

---

## Project Structure

```bash
swarovski-pearl-yield-prediction/
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── README.md
│
├── notebooks/
│   ├── Swarovski_Pearl_Analysis.ipynb
│
├── models/
│   ├── README.md
│
├── src/
│   ├── main.py
│   ├── data_preprocessing.py
│   ├── feature_engineering.py
│   ├── train_model.py
│   ├── evaluate_model.py
│
├── results/
│   ├── plots/
│   ├── metrics/
│
└── reports/
    ├── project_report.md
```

---

# Notebook Structure

The notebook is organized into the following stages:

1. Data Loading & Cleaning
2. Exploratory Data Analysis (EDA)
3. Feature Engineering
4. Feature Selection
5. Model Training
6. Hyperparameter Tuning
7. Model Evaluation
8. Model Explainability (SHAP)
9. Export of Production Artifacts
---

## Models Used

- Linear Regression
- Ridge Regression
- Lasso Regression
- Random Forest Regressor
- K-Nearest Neighbors Regressor
- XGBoost Regressor
- Stacking Ensemble

---

## Results

| Metric | Value |
|---------|------:|
| Best Model | LightGBM |
| R² Score | 0.6601 |
| MAE | 7.9452 |
| RMSE | 10.5418 |

![Learning curve - LightGBM](results/plots/learning_curve.png)

---

## Tech Stack

- Python
- Pandas
- NumPy
- Scikit-learn
- XGBoost
- Optuna
- SHAP
- Matplotlib
- Seaborn

---

## Key Highlights

- End-to-end production-ready machine learning workflow
- Comprehensive exploratory data analysis
- Domain-driven feature engineering
- Leakage-aware preprocessing pipeline
- Time-based validation strategy
- Automated hyperparameter optimization using Optuna
- Model explainability using SHAP
- Exportable production artifacts for deployment

---

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/Soham-2511/swarovski-pearl-yield-prediction.git
cd swarovski-pearl-yield-prediction
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add the proprietary dataset

Place all dataset files inside the `data/` folder.

### 4. Run the notebook

```bash
jupyter notebook notebooks/Swarovski_Pearl_Analysis_Production.ipynb
```

---

## Future Improvements

- Advanced interaction-based feature engineering
- Time-series forecasting of manufacturing yield
- Automated model retraining pipeline
- Model monitoring and drift detection
- REST API deployment
- Interactive manufacturing dashboard

---

## Author

**Soham Jagtap**

B.Tech (Hons.), Metallurgical & Materials Engineering  
Indian Institute of Technology Kharagpur  

- GitHub: https://github.com/Soham-2511
- LinkedIn: https://www.linkedin.com/in/soham-jagtap-8a9977256/

---

## Acknowledgements

This project was developed during my **Data Analyst Internship at Swarovski**. The dataset used is proprietary and has been anonymized for confidentiality. All code and workflows shared in this repository are intended for educational and portfolio purposes.

---

## Support

If you found this project useful or interesting, consider giving this repository a ⭐ on GitHub. It helps others discover the project and motivates future improvements.