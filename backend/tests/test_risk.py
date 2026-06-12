import pandas as pd

from app.analytics.risk import risk_table, segment_for

THRESHOLDS = {
    "pass_mark": 10.0,
    "high_absence_rate": 0.15,
    "performance_drop": 3.0,
    "expected_hours": 200.0,
}


def test_segment_for_boundaries():
    assert segment_for(80, 6, 10) == "a_risque"
    assert segment_for(40, 9, 10) == "fragile"
    assert segment_for(5, 17, 10) == "excellent"
    assert segment_for(5, 14, 10) == "stable"
    assert segment_for(5, 11, 10) == "moyen"


def test_risk_table_flags_low_average_student():
    grades = pd.DataFrame(
        {
            "student_id": [1, 1, 2, 2],
            "value": [6.0, 5.0, 16.0, 17.0],
            "period": ["S1", "S2", "S1", "S2"],
        }
    )
    absences = pd.DataFrame(
        {"student_id": [1], "hours": [40.0], "type": ["absence"]}
    )
    rt = risk_table(grades, absences, THRESHOLDS).set_index("student_id")
    # L'etudiant faible et souvent absent a un risque plus eleve que le bon.
    assert rt.loc[1, "risk_score"] > rt.loc[2, "risk_score"]
    assert rt.loc[1, "segment"] in ("a_risque", "fragile")
    assert rt.loc[2, "segment"] == "excellent"


def test_risk_table_empty():
    rt = risk_table(pd.DataFrame(), pd.DataFrame(), THRESHOLDS)
    assert rt.empty
