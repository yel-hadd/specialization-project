import io

import pandas as pd


def read_file(filename: str, content: bytes) -> pd.DataFrame:
    """Read a CSV or Excel file (as bytes) into a DataFrame based on its extension."""
    name = filename.lower()
    if name.endswith((".xlsx", ".xls")):
        return pd.read_excel(io.BytesIO(content))
    if name.endswith((".csv", ".txt")):
        # Try utf-8 first, then latin-1 for files from a French Excel export
        try:
            return pd.read_csv(io.BytesIO(content))
        except UnicodeDecodeError:
            return pd.read_csv(io.BytesIO(content), encoding="latin-1")
    raise ValueError(f"Type de fichier non supporte : {filename}")
