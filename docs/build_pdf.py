"""Render docs/RAPPORT.md to docs/RAPPORT.pdf.

Markdown -> HTML (with tables) styled by report.css, then HTML -> PDF via WeasyPrint.
Run from anywhere:  python docs/build_pdf.py
Requires: markdown, weasyprint  (pip install markdown weasyprint)
"""

from pathlib import Path

import markdown
from weasyprint import HTML

DOCS = Path(__file__).resolve().parent


def main() -> None:
    md_text = (DOCS / "RAPPORT.md").read_text(encoding="utf-8")
    css = (DOCS / "report.css").read_text(encoding="utf-8")
    body = markdown.markdown(md_text, extensions=["tables", "fenced_code", "sane_lists"])
    html = (
        "<!DOCTYPE html><html lang='fr'><head><meta charset='utf-8'>"
        f"<style>{css}</style></head><body>{body}</body></html>"
    )
    out = DOCS / "RAPPORT.pdf"
    # base_url=DOCS so the relative screenshots/ image paths resolve.
    HTML(string=html, base_url=str(DOCS)).write_pdf(out)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
