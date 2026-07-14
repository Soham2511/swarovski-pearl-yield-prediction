import logging
import pandas as pd
from src.config import CONFIG
from src.data_loader import load_and_merge_excel
from src.preprocess import clean_dataset
from src.feature_engg import engineer_features, drop_high_vif_features, select_top_features_mi
from src.train import train_and_evaluate
import joblib

# Setup Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)-7s | %(message)s")

def main():
    # 1. Ingestion & Preprocessing (from previous step)
    logging.info("Starting Data Pipeline...")
    # NOTE: Replace with a small subset if testing, reading entire excel might take time
    raw_df = load_and_merge_excel(CONFIG["raw_data_path"])
    clean_df = clean_dataset(raw_df, target=CONFIG["target"])
    
    # 2. Feature Engineering
    logging.info("Starting Feature Engineering...")
    fe_df = engineer_features(clean_df)
    
    # Separate Features and Target
    # Drop identifiers that shouldn't be trained on
    drop_cols = CONFIG["id_cols"] + [CONFIG["date_col"], CONFIG["target"]]
    X = fe_df.drop(columns=[c for c in drop_cols if c in fe_df.columns])
    y = fe_df[CONFIG["target"]]
    
    # 3. Feature Selection
    logging.info("Starting Feature Selection...")
    # Multicollinearity pruning
    X_reduced = drop_high_vif_features(X, threshold=CONFIG["vif_threshold"])
    
    # Mutual Information selection
    top_features = select_top_features_mi(X_reduced, y, top_k=CONFIG["top_k_mi_features"])
    X_final = X_reduced[top_features]
    
    # 4. Model Training & Evaluation
    logging.info("Starting Model Training...")
    final_model, cv_results = train_and_evaluate(X_final, y)
    
    # 5. Save the Production Model
    model_path = CONFIG["model_dir"] / "production_stacker_model.pkl"
    CONFIG["model_dir"].mkdir(parents=True, exist_ok=True)
    joblib.dump(final_model, model_path)
    logging.info(f"Pipeline Complete. Model saved to {model_path}")

if __name__ == "__main__":
    main()