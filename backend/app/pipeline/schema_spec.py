"""Expected columns per file type and column-name aliases.

The cleaner normalizes headers to snake_case, then maps known aliases (French and
English variants) to the canonical names used downstream.
"""

# Required columns per import type (canonical names)
REQUIRED_COLUMNS = {
    "students": ["student_code", "first_name", "last_name"],
    "grades": ["student_code", "module_code", "value"],
    "absences": ["student_code", "date", "hours"],
}

# Aliases: normalized header -> canonical name
ALIASES = {
    # student identity
    "code_etudiant": "student_code",
    "code_student": "student_code",
    "matricule": "student_code",
    "id_etudiant": "student_code",
    "prenom": "first_name",
    "firstname": "first_name",
    "nom": "last_name",
    "lastname": "last_name",
    "courriel": "email",
    "mail": "email",
    # class
    "classe": "class_name",
    "class": "class_name",
    "groupe": "class_name",
    "niveau": "level",
    "annee": "academic_year",
    "annee_academique": "academic_year",
    "date_inscription": "enrollment_date",
    # module
    "code_module": "module_code",
    "module": "module_code",
    "nom_module": "module_name",
    "coefficient": "coefficient",
    "coef": "coefficient",
    # grade
    "note": "value",
    "valeur": "value",
    "grade": "value",
    "type_evaluation": "assessment_type",
    "evaluation": "assessment_type",
    "periode": "period",
    "semestre": "period",
    # absence
    "heures": "hours",
    "duree": "hours",
    "justifiee": "justified",
    "justifie": "justified",
    "type_absence": "type",
}


def detect_type(columns: list[str]) -> str | None:
    """Guess the file type from its columns (best effort)."""
    cols = set(columns)
    if {"value"} & cols and {"module_code"} & cols:
        return "grades"
    if {"hours"} & cols:
        return "absences"
    if {"first_name", "last_name"} & cols:
        return "students"
    return None
