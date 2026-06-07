import re

import pandas as pd

from app.pipeline.schema_spec import ALIASES


def _normalize_header(name: str) -> str:
    """Passe un nom de colonne en minuscules, sans accents ni ponctuation, en snake_case."""
    s = str(name).strip().lower()
    accents = str.maketrans("àâäéèêëîïôöùûüç", "aaaeeeeiioouuuc")
    s = s.translate(accents)
    s = re.sub(r"[^a-z0-9]+", "_", s)
    return s.strip("_")


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Normalise les en-tetes puis ramene les alias connus aux noms canoniques."""
    df = df.rename(columns=_normalize_header)
    df = df.rename(columns={c: ALIASES.get(c, c) for c in df.columns})
    return df


def clean(df: pd.DataFrame, dtype: str) -> tuple[pd.DataFrame, list[str]]:
    """Nettoie un DataFrame deja normalise. Renvoie le frame nettoye et les avertissements."""
    warnings: list[str] = []

    before = len(df)
    df = df.drop_duplicates()
    if len(df) < before:
        warnings.append(f"{before - len(df)} doublons supprimes")

    # On enleve les espaces autour des champs texte
    text_cols = [c for c in df.columns if df[c].dtype == object]
    for col in text_cols:
        df[col] = df[col].astype(str).str.strip().replace({"nan": None, "": None})

    if dtype == "grades" and "value" in df.columns:
        df["value"] = pd.to_numeric(df["value"], errors="coerce")
        # Une note doit etre entre 0 et 20 ; le reste est mis a NA puis rejete
        oor = df["value"].between(0, 20) | df["value"].isna()
        if (~oor).any():
            warnings.append(
                f"{(~oor).sum()} notes hors de l'intervalle 0..20 ont ete supprimees"
            )
            df.loc[~oor, "value"] = pd.NA

    if dtype == "absences" and "hours" in df.columns:
        df["hours"] = pd.to_numeric(df["hours"], errors="coerce").fillna(0.0)
        # "oui", "yes", "1"... comptent comme justifie, tout le reste comme non
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

    # Conversion des colonnes de dates ; une date invalide devient NaT
    for col in ("date", "enrollment_date"):
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce").dt.date

    return df, warnings
