"""Generate a teaching report in HTML or PDF (Bonus C)."""

import base64
import io
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # headless backend, no display required
import matplotlib.pyplot as plt  # noqa: E402
from jinja2 import Environment, FileSystemLoader, select_autoescape  # noqa: E402

from app.analytics import service  # noqa: E402
from app.core import messages  # noqa: E402

TEMPLATE_DIR = Path(__file__).parent / "templates"
_env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=select_autoescape(["html"]),
)


def _fig_to_base64(fig) -> str:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=110, bbox_inches="tight")
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode("ascii")


def _distribution_chart(db) -> str | None:
    dist = service.grade_distribution(db)
    if not dist["counts"]:
        return None
    fig, ax = plt.subplots(figsize=(7, 3))
    ax.bar(dist["edges"], dist["counts"], color="#1d4ed8")
    ax.set_xlabel("Tranche de note")
    ax.set_ylabel("Nombre de notes")
    ax.tick_params(axis="x", rotation=90, labelsize=7)
    return _fig_to_base64(fig)


def _class_chart(db) -> str | None:
    classes = service.class_analysis(db)
    if not classes:
        return None
    names = [c["class_name"] for c in classes]
    means = [c["mean"] for c in classes]
    fig, ax = plt.subplots(figsize=(7, 3))
    ax.bar(names, means, color="#0e9488")
    ax.set_ylabel("Moyenne")
    ax.tick_params(axis="x", rotation=30, labelsize=8)
    return _fig_to_base64(fig)


def build_context(db) -> dict:
    seg = service.segmentation_summary(db)
    # The API returns recommendation codes; the (French) report renders them to text.
    at_risk = service.at_risk_students(db)
    for s in at_risk:
        s["recommendations"] = [
            messages.recommendation_text(code, "fr") for code in s["recommendations"]
        ]
    return {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "kpis": service.kpis(db),
        "modules": service.module_analysis(db),
        "segmentation": seg.get("counts", {}),
        "at_risk": at_risk,
        "dist_chart": _distribution_chart(db),
        "class_chart": _class_chart(db),
    }


def render_html(db) -> str:
    template = _env.get_template("report.html")
    return template.render(**build_context(db))


def render_pdf(db) -> bytes:
    from weasyprint import HTML  # imported lazily; heavy dependency

    html = render_html(db)
    return HTML(string=html).write_pdf()
