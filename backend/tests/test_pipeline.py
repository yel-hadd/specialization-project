import pandas as pd

from app.pipeline import cleaner, validator
from app.pipeline.schema_spec import detect_type


def test_normalize_columns_maps_french_aliases():
    df = pd.DataFrame({"Code_Etudiant": [1], "Prénom": ["A"], "Nom": ["B"]})
    out = cleaner.normalize_columns(df)
    assert set(out.columns) == {"student_code", "first_name", "last_name"}


def test_detect_type():
    assert detect_type(["student_code", "module_code", "value"]) == "grades"
    assert detect_type(["student_code", "hours"]) == "absences"
    assert detect_type(["student_code", "first_name", "last_name"]) == "students"


def test_clean_drops_duplicates_and_clamps_grades():
    df = pd.DataFrame(
        {
            "student_code": ["S1", "S1", "S2"],
            "module_code": ["M1", "M1", "M1"],
            "value": [12, 12, 27.5],  # une ligne en doublon, une note hors bornes
        }
    )
    cleaned, warnings = cleaner.clean(df, "grades")
    # Le doublon est retire, il reste 2 lignes.
    assert len(cleaned) == 2
    # La note hors bornes devient NA.
    assert cleaned["value"].isna().sum() == 1
    assert any("doublon" in w.lower() for w in warnings)


def test_validate_missing_required_column():
    df = pd.DataFrame({"student_code": ["S1"]})  # module_code et value manquants
    errors, _ = validator.validate(df, "grades")
    assert errors and "Colonnes obligatoires manquantes" in errors[0]


def test_drop_invalid_rows_counts_rejections():
    df = pd.DataFrame(
        {"student_code": ["S1", None], "module_code": ["M1", "M1"], "value": [10, 11]}
    )
    out, rejected = validator.drop_invalid_rows(df, "grades")
    assert rejected == 1
    assert len(out) == 1
