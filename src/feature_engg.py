import pandas as pd
import numpy as np
import logging
from sklearn.feature_selection import mutual_info_regression
from statsmodels.stats.outliers_influence import variance_inflation_factor

from src.config import CONFIG

logger = logging.getLogger(__name__)

def create_historical_features(df: pd.DataFrame, target: str = 'Okper') -> pd.DataFrame:
    """
    Creates expanding mean (historical average) features grouped by Product and Colour.
    Critically uses .shift(1) so the model only sees past averages, avoiding leakage.
    """
    df = df.copy()
    
    # Ensure data is sorted chronologically if a Date column exists
    if CONFIG["date_col"] in df.columns:
        df = df.sort_values(CONFIG["date_col"])

    # Feature 1: Historical average Okper per ProductNumber
    df['hist_avg_product'] = df.groupby('ProductNumber')[target].transform(
        lambda x: x.expanding().mean().shift(1)
    )
    
    # Feature 2: Historical average Okper per ColourCode
    df['hist_avg_colour'] = df.groupby('ColourCode')[target].transform(
        lambda x: x.expanding().mean().shift(1)
    )

    # Feature 3: Historical average Okper per Product-Colour combination
    df['hist_avg_prod_col'] = df.groupby(['ProductNumber', 'ColourCode'])[target].transform(
        lambda x: x.expanding().mean().shift(1)
    )

    # Fill NaNs created by .shift(1) with the global training mean (to be safe)
    global_mean = df[target].mean()
    df.fillna({'hist_avg_product': global_mean, 
               'hist_avg_colour': global_mean, 
               'hist_avg_prod_col': global_mean}, inplace=True)
               
    logger.info("Historical features created successfully.")
    return df

def drop_high_vif_features(X: pd.DataFrame, threshold: float = 10.0) -> pd.DataFrame:
    """Iteratively removes features with high Variance Inflation Factor (VIF)."""
    # Only calculate VIF for numerical columns
    numeric_df = X.select_dtypes(include=[np.number]).dropna()
    
    dropped = True
    while dropped:
        dropped = False
        vif_data = pd.DataFrame()
        vif_data["feature"] = numeric_df.columns
        vif_data["VIF"] = [variance_inflation_factor(numeric_df.values, i) 
                           for i in range(numeric_df.shape[1])]
        
        max_vif = vif_data['VIF'].max()
        if max_vif > threshold:
            feature_to_drop = vif_data.loc[vif_data['VIF'].idxmax(), 'feature']
            numeric_df = numeric_df.drop(columns=[feature_to_drop])
            X = X.drop(columns=[feature_to_drop])
            logger.info(f"Dropped {feature_to_drop} due to high VIF: {max_vif:.2f}")
            dropped = True

    return X

def select_top_features_mi(X: pd.DataFrame, y: pd.Series, top_k: int = 50) -> list:
    """Selects top K features based on Mutual Information with the target."""
    numeric_X = X.select_dtypes(include=[np.number]).fillna(0)
    
    mi_scores = mutual_info_regression(numeric_X, y, random_state=CONFIG["random_state"])
    mi_series = pd.Series(mi_scores, index=numeric_X.columns)
    
    top_features = mi_series.nlargest(top_k).index.tolist()
    logger.info(f"Selected top {top_k} features using Mutual Information.")
    return top_features

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Master pipeline for Feature Engineering."""
    # 1. Create Time-Series / Expanding features
    df = create_historical_features(df, target=CONFIG["target"])
    
    # Note: Dummy variables/One-Hot encoding should be done here if categorical variables remain
    df = pd.get_dummies(df, columns=['Size'], drop_first=True) 

    return df