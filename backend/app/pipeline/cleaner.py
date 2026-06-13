import re

import pandas as pd

from app.pipeline.schema_spec import ALIASES


def _normalize_header(name: str) -> str:
    """Lowercase a column name, strip accents and punctuation, and convert to snake_case."""
    s = str(name).strip().lower()
    accents = str.maketrans("àâäéèêëîïôöùûüç", "aaaeeeeiioouuuc")
    s = s.translate(accents)
    s = re.sub(r"[^a-z0-9]+", "_", s)
    return s.strip("_")


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize headers, then map known aliases to their canonical names."""
    df = df.rename(columns=_normalize_header)
    df = df.rename(columns={c: ALIASES.get(c, c) for c in df.columns})
    return df


def clean(df: pd.DataFrame, dtype: str) -> tuple[pd.DataFrame, list[str]]:
    """Clean an already-normalized DataFrame. Return the cleaned frame and warnings."""
    warnings: list[str] = []

    before = len(df)
    df = df.drop_duplicates()
    if len(df) < before:
        warnings.append(f"{before - len(df)} doublons supprimes")

    # Strip surrounding whitespace from text fields
    text_cols = [c for c in df.columns if df[c].dtype == object]
    for col in text_cols:
        df[col] = df[col].astype(str).str.strip().replace({"nan": None, "": None})

    if dtype == "grades" and "value" in df.columns:
        df["value"] = pd.to_numeric(df["value"], errors="coerce")
        # A grade must be between 0 and 20; anything else is set to NA and rejected
        oor = df["value"].between(0, 20) | df["value"].isna()
        if (~oor).any():
            warnings.append(
                f"{(~oor).sum()} notes hors de l'intervalle 0..20 ont ete supprimees"
            )
            df.loc[~oor, "value"] = pd.NA

    if dtype == "absences" and "hours" in df.columns:
        df["hours"] = pd.to_numeric(df["hours"], errors="coerce").fillna(0.0)
        # "oui", "yes", "1"... count as justified; everything else as not justified
        if "justified" in df.columns:
            df["justified"] = (
                df["justified"]
                .astype(str)
                .str.lower()
                .isin(["1", "true", "oui", "yes", "y", "o"])
            )
        if "type" in df.columns:
            df["type"] = df["type"].fillna("absence")

    if "coefficient" in df.columns:
        df["coefficient"] = pd.to_numeric(df["coefficient"], errors="coerce").fillna(1.0)

    # Convert date columns; an invalid date becomes NaT
    for col in ("date", "enrollment_date"):
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce").dt.date

    return df, warnings
