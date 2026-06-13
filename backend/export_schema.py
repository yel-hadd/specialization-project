"""Export the database schema as PostgreSQL DDL to schema.sql.

Run from backend/:  python export_schema.py
"""

from pathlib import Path

from sqlalchemy.dialects import postgresql
from sqlalchemy.schema import CreateIndex, CreateTable

from app.core.database import Base
import app.models  # noqa: F401  (populates the metadata)


def main() -> None:
    lines = ["-- EduTrack Analytics - schema PostgreSQL", ""]
    dialect = postgresql.dialect()
    for table in Base.metadata.sorted_tables:
        ddl = str(CreateTable(table).compile(dialect=dialect))
        lines.append(ddl.strip() + ";")
        # Emit the secondary indexes (index=True columns) declared on the models.
        for index in sorted(table.indexes, key=lambda i: i.name or ""):
            lines.append(str(CreateIndex(index).compile(dialect=dialect)).strip() + ";")
        lines.append("")
    out = Path(__file__).parent / "schema.sql"
    out.write_text("\n".join(lines))
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
