from fastapi import APIRouter, Depends, Form, UploadFile, File
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from sqlalchemy.orm import Session
import shutil, os

from app.db import get_db
from app.models import Hero
from app.auth import get_current_admin

router = APIRouter()
templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = "uploads/hero"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# Show Hero Page
@router.get("/admin/hero")
def hero_page(
    request: Request,
    db: Session = Depends(get_db),
    current_admin: str = Depends(get_current_admin)
):
    hero = db.query(Hero).first()   # Get first hero entry
    return templates.TemplateResponse("hero.html", {
        "request": request,
        "hero": hero
    })


# Save/Update Hero
@router.post("/admin/hero")
def save_hero(
    request: Request,
    description: str = Form(...),
    resume_file: UploadFile = File(None),
    image_file: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_admin: str = Depends(get_current_admin)
):
    hero = db.query(Hero).first()
    if not hero:
        hero = Hero()
        db.add(hero)

    hero.description = description

    UPLOAD_DIR = "uploads/hero"
    os.makedirs(UPLOAD_DIR, exist_ok=True)   # make sure folder exists


    UPLOAD_DIR = "uploads/hero"
    os.makedirs(UPLOAD_DIR, exist_ok=True)   # ensure folder exists

    if resume_file and resume_file.filename:   # check filename not empty
        resume_path = os.path.join(UPLOAD_DIR, resume_file.filename)
        with open(resume_path, "wb") as buffer:
            shutil.copyfileobj(resume_file.file, buffer)
        hero.resume_file = resume_path

    if image_file and image_file.filename:    # check filename not empty
        image_path = os.path.join(UPLOAD_DIR, image_file.filename)
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image_file.file, buffer)
        hero.image_file = image_path


    db.commit()
    db.refresh(hero)

    return RedirectResponse(url="/admin/hero", status_code=303)
