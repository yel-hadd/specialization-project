"""Generate synthetic academic data for EduTrack Analytics (French column headers).

Produces, in data/samples/:
  - etudiants.csv   (identity + class)
  - notes.csv       (one row per student/module/period)
  - absences.xlsx   (absences and late arrivals)

plus a set of edge-case files in data/samples/edge_cases/ to exercise the
validation and cleaning pipeline: duplicates, missing values, out-of-range
grades, invalid dates, missing columns, unsupported type, English aliases.

The main files are clean (no broken rows) so the dashboard and screenshots stay
realistic. A latent per-student "ability" correlates grades and absences, giving
analytics an exploitable structure.
"""

from pathlib import Path

import numpy as np
import pandas as pd

SEED = 42
rng = np.random.default_rng(SEED)

OUT = Path(__file__).parent / "samples"
EDGE = OUT / "edge_cases"
OUT.mkdir(parents=True, exist_ok=True)
EDGE.mkdir(parents=True, exist_ok=True)

CLASSES = [
    {"nom": "B1-INFO", "niveau": "Bachelor 1", "annee": "2025-2026"},
    {"nom": "B2-INFO", "niveau": "Bachelor 2", "annee": "2025-2026"},
    {"nom": "B3-DATA", "niveau": "Bachelor 3", "annee": "2025-2026"},
    {"nom": "M1-DATA", "niveau": "Master 1", "annee": "2025-2026"},
]

MODULES = [
    ("MATH101", "Mathematiques", 3),
    ("ALGO102", "Algorithmique", 3),
    ("STAT201", "Statistiques", 2),
    ("DB202", "Bases de donnees", 2),
    ("ML301", "Machine Learning", 4),
    ("WEB203", "Developpement Web", 2),
    ("ENG100", "Anglais", 1),
    ("COMM110", "Communication", 1),
]

PERIODES = ["S1", "S2"]
PRENOMS = ["Yassine", "Sara", "Mehdi", "Lina", "Omar", "Salma", "Anas", "Nada",
           "Reda", "Imane", "Youssef", "Hajar", "Ayoub", "Khadija", "Bilal", "Aya"]
NOMS = ["El Haddad", "Benali", "Cherkaoui", "Idrissi", "Bennani", "Alaoui",
        "Tazi", "Fassi", "Saidi", "Berrada", "Lahlou", "Naciri"]


def make_students(n_per_class: int = 30) -> pd.DataFrame:
    rows = []
    sid = 1
    for cls in CLASSES:
        for _ in range(n_per_class):
            prenom = rng.choice(PRENOMS)
            nom = rng.choice(NOMS)
            rows.append({
                "code_etudiant": f"STU{sid:04d}",
                "prenom": prenom,
                "nom": nom,
                "courriel": f"{prenom.lower()}.{nom.split()[0].lower()}{sid}@edu.ma",
                "classe": cls["nom"],
                "niveau": cls["niveau"],
                "annee": cls["annee"],
                "ability": float(np.clip(rng.normal(12, 3), 4, 19)),  # latent, dropped later
            })
            sid += 1
    return pd.DataFrame(rows)


def make_grades(students: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, s in students.iterrows():
        ability = s["ability"]
        # A per-student S2 shift (consistent across modules) so the whole cohort
        # shows a real period-to-period trend, not just the planted at-risk group.
        # Slightly negative on average, but some students improve.
        s2_shift = float(rng.normal(-0.4, 1.3))
        for code, nom_module, coef in MODULES:
            for periode in PERIODES:
                trend = s2_shift if periode == "S2" else 0.0
                note = float(np.clip(rng.normal(ability + trend, 2.0), 0, 20))
                rows.append({
                    "code_etudiant": s["code_etudiant"],
                    "code_module": code,
                    "nom_module": nom_module,
                    "coefficient": coef,
                    "note": round(note, 2),
                    "evaluation": rng.choice(["DS", "Projet", "Examen"]),
                    "periode": periode,
                })
    return pd.DataFrame(rows)


def make_absences(students: pd.DataFrame) -> pd.DataFrame:
    rows = []
    base = pd.Timestamp("2025-09-15")
    for _, s in students.iterrows():
        rate = max(0.0, (13 - s["ability"]) / 13)
        n_events = rng.poisson(2 + rate * 8)
        for _ in range(n_events):
            day = base + pd.Timedelta(days=int(rng.integers(0, 180)))
            retard = rng.random() < 0.3
            rows.append({
                "code_etudiant": s["code_etudiant"],
                "code_module": rng.choice([m[0] for m in MODULES]),
                "date": day.strftime("%Y-%m-%d"),
                "heures": round(float(rng.choice([1, 2, 3, 4])), 1),
                "type_absence": "retard" if retard else "absence",
                "justifiee": rng.choice(["oui", "non"], p=[0.4, 0.6]),
            })
    return pd.DataFrame(rows)


def make_at_risk_profiles(start_id: int):
    """Build a few extreme students so every case shows up in the dashboard:
    low average (a_risque segment + low_average alert), many absences
    (high_absence alert + absence outlier), and an S1->S2 drop
    (performance_drop alert).
    """
    students, grades, absences = [], [], []
    base = pd.Timestamp("2025-09-15")
    profiles = [
        ("Yassir", "Drissi", "B1-INFO"),
        ("Salwa", "Kabbaj", "B2-INFO"),
        ("Hamza", "Ouali", "B3-DATA"),
        ("Nora", "Sefiani", "M1-DATA"),
        ("Karim", "Belkadi", "B1-INFO"),
    ]
    for i, (prenom, nom, classe) in enumerate(profiles):
        sid = start_id + i
        code = f"STU{sid:04d}"
        niveau = {"B1-INFO": "Bachelor 1", "B2-INFO": "Bachelor 2",
                  "B3-DATA": "Bachelor 3", "M1-DATA": "Master 1"}[classe]
        students.append({
            "code_etudiant": code, "prenom": prenom, "nom": nom,
            "courriel": f"{prenom.lower()}.{nom.lower()}{sid}@edu.ma",
            "classe": classe, "niveau": niveau, "annee": "2025-2026",
        })
        for code_module, nom_module, coef in MODULES:
            s1 = round(float(np.clip(rng.normal(7.5, 1.0), 0, 20)), 2)
            s2 = round(float(np.clip(rng.normal(3.5, 1.0), 0, 20)), 2)
            grades.append({"code_etudiant": code, "code_module": code_module,
                           "nom_module": nom_module, "coefficient": coef,
                           "note": s1, "evaluation": "Examen", "periode": "S1"})
            grades.append({"code_etudiant": code, "code_module": code_module,
                           "nom_module": nom_module, "coefficient": coef,
                           "note": s2, "evaluation": "Examen", "periode": "S2"})
        for _ in range(int(rng.integers(13, 18))):  # roughly 45 to 65 hours total
            day = base + pd.Timedelta(days=int(rng.integers(0, 180)))
            absences.append({
                "code_etudiant": code,
                "code_module": rng.choice([m[0] for m in MODULES]),
                "date": day.strftime("%Y-%m-%d"),
                "heures": round(float(rng.choice([3, 4])), 1),
                "type_absence": rng.choice(["absence", "retard"], p=[0.8, 0.2]),
                "justifiee": "non",
            })
    return pd.DataFrame(students), pd.DataFrame(grades), pd.DataFrame(absences)


def write_edge_cases() -> None:
    """Write small files, each covering one validation or cleaning rule."""
    # Duplicate grade rows.
    pd.DataFrame({
        "code_etudiant": ["STU0001", "STU0001", "STU0002"],
        "code_module": ["MATH101", "MATH101", "MATH101"],
        "note": [12, 12, 8],
        "periode": ["S1", "S1", "S1"],
    }).to_csv(EDGE / "notes_doublons.csv", index=False)

    # Out-of-range and non-numeric grades.
    pd.DataFrame({
        "code_etudiant": ["STU0001", "STU0002", "STU0003"],
        "code_module": ["MATH101", "MATH101", "MATH101"],
        "note": [27, "abc", 14],
        "periode": ["S1", "S1", "S1"],
    }).to_csv(EDGE / "notes_hors_bornes.csv", index=False)

    # Missing required values (empty code_etudiant / note).
    pd.DataFrame({
        "code_etudiant": ["STU0001", "", "STU0003"],
        "code_module": ["MATH101", "MATH101", "MATH101"],
        "note": [12, 10, None],
        "periode": ["S1", "S1", "S1"],
    }).to_csv(EDGE / "notes_valeurs_manquantes.csv", index=False)

    # Students file missing the required 'nom' column.
    pd.DataFrame({
        "code_etudiant": ["STU9001", "STU9002"],
        "prenom": ["Test", "Essai"],
        "classe": ["B1-INFO", "B1-INFO"],
    }).to_csv(EDGE / "etudiants_colonne_manquante.csv", index=False)

    # Absences with an invalid date.
    pd.DataFrame({
        "code_etudiant": ["STU0001", "STU0002"],
        "date": ["2025-11-13", "date-invalide"],
        "heures": [4, 2],
        "type_absence": ["absence", "retard"],
    }).to_excel(EDGE / "absences_date_invalide.xlsx", index=False)

    # English aliases: must still map to the internal columns.
    pd.DataFrame({
        "student_code": ["STU8001", "STU8002"],
        "first_name": ["Alan", "Grace"],
        "last_name": ["Turing", "Hopper"],
        "class": ["B3-DATA", "B3-DATA"],
    }).to_csv(EDGE / "etudiants_alias_anglais.csv", index=False)

    # Unsupported file type.
    (EDGE / "fichier_invalide.json").write_text('{"foo": "bar"}')


def main() -> None:
    students = make_students()
    grades = make_grades(students)
    absences = make_absences(students)

    # Add a small at-risk cohort so the dashboard shows every case.
    ar_students, ar_grades, ar_absences = make_at_risk_profiles(len(students) + 1)
    students_out = pd.concat(
        [students.drop(columns=["ability"]), ar_students], ignore_index=True
    )
    grades = pd.concat([grades, ar_grades], ignore_index=True)
    absences = pd.concat([absences, ar_absences], ignore_index=True)
    students_out.to_csv(OUT / "etudiants.csv", index=False)
    grades.to_csv(OUT / "notes.csv", index=False)
    absences.to_excel(OUT / "absences.xlsx", index=False)
    write_edge_cases()

    print(f"Wrote {len(students_out)} etudiants -> {OUT / 'etudiants.csv'}")
    print(f"Wrote {len(grades)} notes -> {OUT / 'notes.csv'}")
    print(f"Wrote {len(absences)} absences -> {OUT / 'absences.xlsx'}")
    print(f"Wrote edge-case files -> {EDGE}/")
    for f in sorted(EDGE.iterdir()):
        print(f"  - {f.name}")


if __name__ == "__main__":
    main()
