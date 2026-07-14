import pandas as pd
import logging

logger = logging.getLogger(__name__)

def load_and_merge_excel(path: str, sort_by: str | None = None, ascending: bool = True) -> pd.DataFrame:
    """
    Load every sheet of an Excel workbook and concatenate them into one long DataFrame.
    """
    xls = pd.ExcelFile(path)
    frames = []
    for sheet_name in xls.sheet_names:
        sheet_df = pd.read_excel(path, sheet_name=sheet_name)
        sheet_df["__source_sheet"] = sheet_name
        frames.append(sheet_df)
        logger.info("Loaded sheet '%s' -> %s rows, %s cols", sheet_name, *sheet_df.shape)

    merged = pd.concat(frames, ignore_index=True)

    if sort_by is not None and sort_by in merged.columns:
        merged = merged.sort_values(by=sort_by, ascending=ascending)

    logger.info("Merged workbook '%s': final shape %s", path, merged.shape)
    return merged

def load_dictionary(path: str):
    """
    Load the 3 reference sheets: column glossary, colour codes, product codes.
    """
    dictionary = pd.read_excel(path, sheet_name=0)
    colour_code = pd.read_excel(path, sheet_name=1)
    product_code = pd.read_excel(path, sheet_name=2)
    return dictionary, colour_code, product_code