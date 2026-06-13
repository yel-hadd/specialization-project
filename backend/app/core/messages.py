"""User-facing message catalogs (FR/EN) for the codes returned by the API.

The API returns language-neutral codes (recommendation codes, alert types) plus
the numeric values that go with them; the frontend renders them in the language
the user picked. This module holds the server-side rendering used by the generated
PDF/HTML report (French), and is the canonical reference the frontend dictionary
mirrors.
"""

RECOMMENDATIONS = {
    "personalized_support": {
        "fr": "Mettre en place un suivi personnalise et un soutien sur les modules faibles.",
        "en": "Set up personalized tutoring and support on the weak modules.",
    },
    "attendance_reminder": {
        "fr": "Envoyer un rappel d'assiduite et contacter l'etudiant.",
        "en": "Send an attendance reminder and reach out to the student.",
    },
    "analyze_drop": {
        "fr": "Analyser la baisse recente de performance et proposer un point individuel.",
        "en": "Review the recent performance drop and offer a one-on-one meeting.",
    },
    "stable": {
        "fr": "Situation stable, poursuivre le suivi habituel.",
        "en": "Stable situation, keep up the regular monitoring.",
    },
}

ALERT_TEMPLATES = {
    "low_average": {
        "fr": "Moyenne faible ({value}) sous le seuil de {threshold}.",
        "en": "Low average ({value}), below the pass mark of {threshold}.",
    },
    "high_absence": {
        "fr": "Taux d'absence eleve ({value}%).",
        "en": "High absence rate ({value}%).",
    },
    "performance_drop": {
        "fr": "Baisse de performance de {value} points entre les periodes.",
        "en": "Performance drop of {value} points between periods.",
    },
}


def recommendation_text(code: str, lang: str = "fr") -> str:
    entry = RECOMMENDATIONS.get(code)
    if not entry:
        return code
    return entry.get(lang, entry["fr"])


def alert_text(alert_type: str, lang: str = "fr", **params) -> str:
    entry = ALERT_TEMPLATES.get(alert_type)
    if not entry:
        return alert_type
    template = entry.get(lang, entry["fr"])
    try:
        return template.format(**params)
    except (KeyError, IndexError):
        return template
