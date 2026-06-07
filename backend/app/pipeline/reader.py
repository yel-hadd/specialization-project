import io

import pandas as pd


def read_file(filename: str, content: bytes) -> pd.DataFrame:
    """Lit un CSV ou un Excel (en bytes) vers un DataFrame selon l'extension."""
    name = filename.lower()
    if name.endswith((".xlsx", ".xls")):
        return pd.read_excel(io.BytesIO(content))
    if name.endswith((".csv", ".txt")):
        # utf-8 d'abord, puis latin-1 si le fichier vient d'un export Excel francais
        try:
            return pd.read_csv(io.BytesIO(content))
        except UnicodeDecodeError:
            return pd.read_csv(io.BytesIO(content), encoding="latin-1")
        try:
            return pd.read_csv(io.BytesIO(content))
        except UnicodeDecodeError:
            return pd.read_csv(io.BytesIO(content), encoding="latin-1")
    raise ValueError(f"Type de fichier non supporte : {filename}")
