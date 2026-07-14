import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

def parse_art_code(df: pd.DataFrame) -> pd.DataFrame:
    """Split the 'Art' code (e.g. `A.1234.MM4.5`) into ProductNumber and Size."""
    df = df.copy()
    extracted = df["Art"].str.extract(r"A\.(\d+)\.MM([\d\.]+)")
    df["ProductNumber"] = pd.to_numeric(extracted[0], errors="coerce").astype("Float64")

    size_raw = extracted[1].str.replace(r"^\.+", "", regex=True)
    size_raw = size_raw.str.replace(r"\.+", ".", regex=True)
    df["Size"] = pd.to_numeric(size_raw, errors="coerce").astype("Float64")

    n_unparsed = df["ProductNumber"].isna().sum()
    if n_unparsed:
        logger.warning("%d rows failed Art-code parsing (unexpected format)", n_unparsed)
    return df

def clean_colour_code(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the ColourCode column and ensure it is numeric."""
    df = df.rename(columns={"Code": "ColourCode"}).copy()
    df = df[~df["ColourCode"].astype(str).str.strip().isin(["ng", "nd"])].copy()
    df["ColourCode"] = (
        df["ColourCode"].astype(str).str.replace(".0", "", regex=False).replace("nan", np.nan)
    )
    df["ColourCode"] = pd.to_numeric(df["ColourCode"], errors="coerce").astype("Float64")
    return df

def remove_leaky_and_redundant_cols(df: pd.DataFrame) -> pd.DataFrame:
    """Removes columns known after production and redundant identifiers."""
    # 1. Defect codes
    defect_cols = [col for col in df.columns if col.startswith(('a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1'))]

    # 2. Hardcoded leaky variables
    leaky_cols = [
        'OkQty', 'GDkg', 'RCDkg', 'PackedDate', 'GDNos', 'RCDNos', 'QtyPer', 'BatchNo',
        'GDper', 'RCDper', 'totqtyno', 'PackMonth', 'Packyr', 'Loss', '__source_sheet'
    ]

    # 3. Redundant variables
    redundant_cols = ['Art', 'ProductDesc', 'ColourDesc']

    cols_to_drop = defect_cols + leaky_cols + redundant_cols
    existing_cols_to_drop = [c for c in cols_to_drop if c in df.columns]

    return df.drop(columns=existing_cols_to_drop)

def clean_dataset(df: pd.DataFrame, target: str = 'Okper') -> pd.DataFrame:
    """Full cleaning pipeline. Returns a clean, de-duplicated, leakage-free DataFrame."""
    n0 = len(df)

    df = clean_colour_code(df)
    df = parse_art_code(df)

    for col in ["ProductNumber", "ColourCode", "RBFA", "SysNo", "BatchNo"]:
        if col in df.columns:
            df[col] = df[col].astype(str)

    df = df.dropna(subset=["Size", target]).copy()
    df = df[(df[target] >= 0) & (df[target] <= 100)].copy()
    
    df = remove_leaky_and_redundant_cols(df)

    n_dupes = df.duplicated().sum()
    if n_dupes:
        logger.warning("Dropping %d exact duplicate rows", n_dupes)
        df = df.drop_duplicates()

    # Standardize column order 
    front_cols = [c for c in ["ProductNumber", "Size", "ColourCode", "BatchNo", "SysNo"] if c in df.columns]
    other_cols = [c for c in df.columns if c not in front_cols and c != target]

    df = df[front_cols + other_cols + [target]]

    logger.info("Cleaning: %d -> %d rows (%.1f%% kept)", n0, len(df), 100 * len(df) / n0)
    return df.reset_index(drop=True)

def data_quality_report(df: pd.DataFrame) -> pd.DataFrame:
    """Generate a high-level summary of missing values and datatypes."""
    report = pd.DataFrame({
        "dtype": df.dtypes.astype(str),
        "n_missing": df.isna().sum(),
        "pct_missing": (100 * df.isna().mean()).round(2),
        "n_unique": df.nunique(),
    }).sort_values("pct_missing", ascending=False)
    return report