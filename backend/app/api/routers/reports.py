from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse, Response
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models import User
from app.reports import generator

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/html", response_class=HTMLResponse)
def report_html(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return HTMLResponse(content=generator.render_html(db))


@router.get("/pdf")
def report_pdf(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    pdf = generator.render_pdf(db)
    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=rapport_edutrack.pdf"},
    )
