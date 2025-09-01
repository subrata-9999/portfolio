from fastapi import APIRouter, Depends, Form, UploadFile, File
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from sqlalchemy.orm import Session
import shutil, os

from app.db import get_db
from app.models import About
from app.auth import get_current_admin

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/admin/about")
def get_about(request: Request,
    db: Session = Depends(get_db),
    current_admin: str = Depends(get_current_admin)
):
    about = db.query(About).first()
    return templates.TemplateResponse("admin_about.html", {"request": request, "about": about})


@router.post("/admin/about")
def save_about(
    request: Request,
    des1: str = Form(...),
    des2: str = Form(...),
    db: Session = Depends(get_db),
    current_admin: str = Depends(get_current_admin)
):
    about = db.query(About).first()

    if about:
        about.des1 = des1
        about.des2 = des2
    else:
        about = About(des1=des1, des2=des2)
        db.add(about)

    db.commit()
    return RedirectResponse(url="/admin/about", status_code=303)
