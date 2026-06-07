import pandas as pd

from app.pipeline.schema_spec import REQUIRED_COLUMNS


def validate(df: pd.DataFrame, dtype: str) -> tuple[list[str], list[str]]:
    """Verifie les colonnes obligatoires et les valeurs requises.

    Renvoie (erreurs, avertissements). Une erreur bloque l'import, un avertissement
    est juste informatif.
    """
    errors: list[str] = []
    warnings: list[str] = []

    required = REQUIRED_COLUMNS.get(dtype, [])
    missing = [c for c in required if c not in df.columns]
    if missing:
        errors.append(f"Colonnes obligatoires manquantes : {', '.join(missing)}")
        return errors, warnings

    for col in required:
        n_null = int(df[col].isna().sum())
        if n_null:
            warnings.append(
                f"{n_null} lignes ont un champ '{col}' manquant et seront ignorees"
            )

    return errors, warnings


def drop_invalid_rows(df: pd.DataFrame, dtype: str) -> tuple[pd.DataFrame, int]:
    """Supprime les lignes ou un champ obligatoire manque. Renvoie (frame, nb_rejetees)."""
    required = REQUIRED_COLUMNS.get(dtype, [])
    before = len(df)
    df = df.dropna(subset=[c for c in required if c in df.columns])
    return df, before - len(df)
