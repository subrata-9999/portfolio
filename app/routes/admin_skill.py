from fastapi import APIRouter, Request, Form, Depends, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
import os, re
from app.db import get_db
from app.models import Skill, SkillStatus
from fastapi.templating import Jinja2Templates
from typing import Optional
from app.auth import get_current_admin


router = APIRouter(prefix="/admin/skills", tags=["Admin Skills"])

templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = "uploads/skills"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# Custom secure filename (no need for werkzeug)
def secure_filename(filename: str) -> str:
    filename = os.path.basename(filename)  # remove any directory path
    return re.sub(r'[^a-zA-Z0-9_.-]', '_', filename)  # keep safe chars only


# Show skills page
@router.get("/", response_class=HTMLResponse)
def show_skills(request: Request, db: Session = Depends(get_db), current_admin: str = Depends(get_current_admin)):
    skills = db.query(Skill).all()
    return templates.TemplateResponse(
        "admin_skill.html",
        {"request": request, "skills": skills}
    )


@router.post("/save")
async def save_skill(
    request: Request,
    db: Session = Depends(get_db),
    current_admin: str = Depends(get_current_admin),
    id: Optional[str] = Form(None),   # accept string or None
    name: str = Form(...),
    status: str = Form("a"),
    image_file: UploadFile = File(None)
):
    filename = None

    # save file if uploaded
    if image_file and image_file.filename.strip():  # <-- check filename
        filename = image_file.filename
        os.makedirs(UPLOAD_DIR, exist_ok=True)      # <-- ensure folder exists
        filepath = os.path.join(UPLOAD_DIR, filename)
        with open(filepath, "wb") as buffer:
            buffer.write(image_file.file.read())


    # Convert id properly
    skill_id = int(id) if id and id.isdigit() else None

    if skill_id:  # Update existing
        skill = db.query(Skill).filter(Skill.id == skill_id).first()
        if skill:
            skill.name = name
            skill.status = SkillStatus(status)
            if filename:  # <-- only update image if a new file uploaded
                skill.image_file = filename
            db.commit()
    else:  # Add new
        new_skill = Skill(name=name, image_file=filename, status=SkillStatus(status))
        db.add(new_skill)
        db.commit()

    return RedirectResponse(url="/admin/skills/", status_code=303)