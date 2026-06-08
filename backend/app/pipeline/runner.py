import json

from sqlalchemy.orm import Session

from app.models import ImportLog
from app.pipeline import cleaner, loader, reader, validator
from app.pipeline.schema_spec import detect_type


def run_import(
    db: Session, filename: str, content: bytes, dtype: str | None
) -> dict:
    """Enchaine tout le pipeline : lecture, validation, nettoyage, chargement, journalisation.

    Renvoie un resume conforme au schema ImportResult.
    """
    errors: list[str] = []
    warnings: list[str] = []
    rows_processed = 0
    rows_rejected = 0
    status = "success"

    try:
        df = reader.read_file(filename, content)
        df = cleaner.normalize_columns(df)

        if not dtype or dtype == "auto":
            dtype = detect_type(list(df.columns))
        if not dtype:
            raise ValueError(
                "Impossible de detecter le type de fichier a partir des colonnes"
            )

        v_errors, v_warnings = validator.validate(df, dtype)
        errors += v_errors
        warnings += v_warnings

        if not errors:
            df, clean_warnings = cleaner.clean(df, dtype)
            warnings += clean_warnings
            df, rejected = validator.drop_invalid_rows(df, dtype)
            rows_rejected += rejected
            rows_processed = loader.load(db, df, dtype)
            status = "partial" if rows_rejected else "success"
        else:
            status = "failed"
    except Exception as exc:  # noqa: BLE001 - on garde la trace de toute erreur dans le log
        errors.append(str(exc))
        status = "failed"
        rows_processed = 0
        dtype = dtype or "unknown"

    # En cas d'echec, on annule les ecritures partielles avant de journaliser l'import
    if status == "failed":
        db.rollback()

    log = ImportLog(
        filename=filename,
        type=dtype,
        rows_processed=rows_processed,
        rows_rejected=rows_rejected,
        status=status,
        error_log=json.dumps({"errors": errors, "warnings": warnings}),
    )
    db.add(log)
    db.commit()
    db.refresh(log)

    return {
        "import_id": log.id,
        "filename": filename,
        "type": dtype,
        "rows_processed": rows_processed,
        "rows_rejected": rows_rejected,
        "status": status,
        "errors": errors,
        "warnings": warnings,
    }
