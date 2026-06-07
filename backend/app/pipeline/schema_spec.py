"""Colonnes attendues par type de fichier et alias de noms de colonnes.

Le cleaner normalise les en-tetes en snake_case, puis ramene les alias connus
(variantes francaises et anglaises) vers les noms canoniques utilises ensuite.
"""

# Colonnes obligatoires par type d'import (noms canoniques)
REQUIRED_COLUMNS = {
    "students": ["student_code", "first_name", "last_name"],
    "grades": ["student_code", "module_code", "value"],
    "absences": ["student_code", "date", "hours"],
}

# Alias : en-tete normalise -> nom canonique
ALIASES = {
    # identite etudiant
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
    # classe
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
    # note
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
    """Devine le type de fichier a partir de ses colonnes (au mieux)."""
    cols = set(columns)
    if {"value"} & cols and {"module_code"} & cols:
        return "grades"
    if {"hours"} & cols:
        return "absences"
    if {"first_name", "last_name"} & cols:
        return "students"
    return None
