"""Export the database schema as PostgreSQL DDL to schema.sql.

Run from backend/:  python export_schema.py
"""

from pathlib import Path

from sqlalchemy.dialects import postgresql
from sqlalchemy.schema import CreateTable

from app.core.database import Base
import app.models  # noqa: F401  (populates the metadata)


def main() -> None:
    lines = ["-- EduTrack Analytics - schema PostgreSQL", ""]
    for table in Base.metadata.sorted_tables:
        ddl = str(CreateTable(table).compile(dialect=postgresql.dialect()))
        lines.append(ddl.strip() + ";")
        lines.append("")
    out = Path(__file__).parent / "schema.sql"
    out.write_text("\n".join(lines))
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
