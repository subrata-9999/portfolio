from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from typing import Optional

from app.db import get_db
from app.models import Link, SkillStatus
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/admin/links", tags=["Admin Links"])
templates = Jinja2Templates(directory="templates")

# -----------------------------
# Show all links
# -----------------------------
@router.get("/", response_class=HTMLResponse)
def show_links(request: Request, db: Session = Depends(get_db)):
    links = db.query(Link).all()
    return templates.TemplateResponse("admin_link.html", {"request": request, "links": links})

# -----------------------------
# Add/Update link
# -----------------------------

@router.post("/save")
def save_link(
    request: Request,
    db: Session = Depends(get_db),
    id: Optional[str] = Form(None),  # <-- change here
    key: str = Form(...),
    value: str = Form(...),
    status: str = Form("a")
):
    link_id = int(id) if id and id.isdigit() else None  # safe conversion

    if link_id:  # update
        link = db.query(Link).filter(Link.id == link_id).first()
        if link:
            link.key = key
            link.value = value
            link.status = SkillStatus(status)
            db.commit()
    else:  # add new
        new_link = Link(key=key, value=value, status=SkillStatus(status))
        db.add(new_link)
        db.commit()

    return RedirectResponse(url="/admin/links/", status_code=303)