import pandas as pd
import numpy as np
import logging
from sklearn.model_selection import TimeSeriesSplit, KFold, cross_validate
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.ensemble import StackingRegressor, RandomForestRegressor
from sklearn.linear_model import Ridge
import lightgbm as lgb
import xgboost as xgb

from src.config import CONFIG

logger = logging.getLogger(__name__)

def evaluate_model(y_true, y_pred, dataset_name="Test"):
    """Calculates and logs standard regression metrics."""
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    
    logger.info(f"--- {dataset_name} Evaluation ---")
    logger.info(f"RMSE: {rmse:.4f}")
    logger.info(f"MAE:  {mae:.4f}")
    logger.info(f"R2:   {r2:.4f}")
    return {"rmse": rmse, "mae": mae, "r2": r2}

def build_stacking_regressor():
    """
    Builds the crash-proof Stacking Regressor.
    Uses KFold(shuffle=False) for the inner loop to maintain time order 
    without triggering the TimeSeriesSplit partition error.
    """
    base_models = [
        ('lgb', lgb.LGBMRegressor(random_state=CONFIG["random_state"])),
        ('xgb', xgb.XGBRegressor(random_state=CONFIG["random_state"], objective='reg:squarederror')),
        ('rf',  RandomForestRegressor(n_estimators=100, random_state=CONFIG["random_state"]))
    ]
    
    # The Inner Loop Fix: KFold without shuffle acts as a safe sequential chunker
    inner_cv = KFold(n_splits=5, shuffle=False)
    
    meta_model = Ridge(alpha=1.0)
    
    stacker = StackingRegressor(
        estimators=base_models,
        final_estimator=meta_model,
        cv=inner_cv,
        passthrough=False
    )
    return stacker

def train_and_evaluate(X: pd.DataFrame, y: pd.Series):
    """
    Evaluates the model using a strict TimeSeriesSplit (Outer Loop) 
    to honestly mimic production deployment.
    """
    logger.info("Initializing Stacking Regressor...")
    model = build_stacking_regressor()
    
    # Outer Loop: Strict TimeSeries evaluation
    tscv = TimeSeriesSplit(n_splits=CONFIG["n_cv_splits"])
    
    logger.info("Running Time-Series Cross Validation...")
    cv_results = cross_validate(
        model, X, y, 
        cv=tscv, 
        scoring=('r2', 'neg_mean_squared_error', 'neg_mean_absolute_error'),
        return_train_score=True,
        n_jobs=-1
    )
    
    # Log CV Results
    mean_r2 = cv_results['test_r2'].mean()
    mean_rmse = np.sqrt(-cv_results['test_neg_mean_squared_error'].mean())
    logger.info(f"CV Test R2 Score: {mean_r2:.4f}")
    logger.info(f"CV Test RMSE: {mean_rmse:.4f}")
    
    # Final Fit on all data for production deployment
    logger.info("Fitting final model on all data...")
    model.fit(X, y)
    
    return model, cv_results