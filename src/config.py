import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
MODEL_DIR = BASE_DIR / "models"
REPORT_DIR = BASE_DIR / "reports"

RANDOM_STATE = 42

CONFIG = {
    # ---- data sources ------------------------------------------------
    "raw_data_path": RAW_DATA_DIR / "CP Results 2018 to 6_2024.xlsx",
    "dictionary_path": DATA_DIR / "dictionary" / "Swarovski_dictionary.xlsx",
    "processed_dir": PROCESSED_DATA_DIR,
    "report_dir": REPORT_DIR,
    "model_dir": MODEL_DIR,

    # ---- schema --------------------------------------------------------
    "target": "Okper",
    "date_col": "SFInDate",
    "id_cols": ["Art", "SysNo", "BatchNo", "RBFA"],
    "group_cols": ["ProductNumber", "ColourCode"],   

    "glass_defects":    ["a110", "b110", "c110", "d110", "e110"],
    "coating_defects":  ["a111", "b111", "c111", "d111", "e111", "f111", "g111", "h111"],
    "removing_defects": ["a112", "b112", "c112", "d112"],

    # Columns known *after* production that cause Data Leakage
    "post_outcome_leak_cols": [
        "Loss", "GDkg", "RCDkg", "PackMonth", "Packyr",
    ],

    # ---- splitting -------------------------------------------------------
    "test_size": 0.2,
    "n_cv_splits": 3,
    "random_state": RANDOM_STATE,

    # ---- feature engineering -------------------------------------------
    "rolling_window": 3,

    # ---- feature selection -----------------------------------------------
    "corr_drop_threshold": 0.95,   
    "vif_threshold": 10.0,
    "top_k_mi_features": 60,       

    # ---- misc ---------------------------------------------------------
    "n_optuna_trials": 40,
}