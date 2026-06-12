import pandas as pd

from app.analytics import anomalies, descriptive


def test_grade_outlier_detected():
    # 9 grades around 12, one extreme low at 1 -> flagged by z-score.
    grades = pd.DataFrame(
        {
            "student_id": list(range(1, 11)),
            "student_code": [f"S{i}" for i in range(1, 11)],
            "module_id": [1] * 10,
            "module_name": ["Math"] * 10,
            "value": [12, 12, 13, 11, 12, 13, 12, 11, 12, 1],
        }
    )
    out = anomalies.grade_outliers(grades)
    assert any(o["value"] == 1 for o in out)


def test_absence_outlier_detected():
    absences = pd.DataFrame(
        {
            "student_id": [1, 2, 3, 4, 5],
            "student_code": [f"S{i}" for i in range(1, 6)],
            "hours": [2, 3, 2, 4, 80],  # one student far above the rest
        }
    )
    out = anomalies.absence_outliers(absences)
    assert any(o["absence_hours"] == 80 for o in out)


def test_distribution_buckets_sum_to_count():
    grades = pd.DataFrame({"value": [0, 5, 5, 10, 15, 19.9]})
    dist = descriptive.distribution(grades)
    assert len(dist["edges"]) == 20
    assert sum(dist["counts"]) == len(grades)


def test_empty_inputs_are_safe():
    assert anomalies.grade_outliers(pd.DataFrame()) == []
    assert anomalies.absence_outliers(pd.DataFrame()) == []
    assert descriptive.distribution(pd.DataFrame()) == {"edges": [], "counts": []}
