from fastapi import APIRouter, Request, Form, Depends, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
import os
from typing import Optional

from app.db import get_db
from app.models import Project, SkillStatus
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/admin/projects", tags=["Admin Projects"])
templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = "uploads/projects"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# -----------------------------
# Show all projects
# -----------------------------
@router.get("/", response_class=HTMLResponse)
def show_projects(request: Request, db: Session = Depends(get_db)):
    projects = db.query(Project).all()
    return templates.TemplateResponse("admin_project.html", {"request": request, "projects": projects})


# -----------------------------
# Add / Update project
# -----------------------------
@router.post("/save")
async def save_project(
    request: Request,
    db: Session = Depends(get_db),
    id: Optional[str] = Form(None),
    name: str = Form(...),
    description: str = Form(...),
    project_url: str = Form(None),
    status: str = Form("a"),
    image_file: UploadFile = File(None)
):
    filename = None

    # save uploaded file
    if image_file:
        filename = image_file.filename
        filepath = os.path.join(UPLOAD_DIR, filename)
        with open(filepath, "wb") as buffer:
            buffer.write(image_file.file.read())

    # Convert id properly
    project_id = int(id) if id and id.isdigit() else None

    if project_id:  # update existing
        project = db.query(Project).filter(Project.id == project_id).first()
        if project:
            project.name = name
            project.description = description
            project.project_url = project_url
            project.status = SkillStatus(status)
            if filename:
                project.image_file = filename
            db.commit()
    else:  # add new
        new_project = Project(
            name=name,
            description=description,
            project_url=project_url,
            image_file=filename,
            status=SkillStatus(status)
        )
        db.add(new_project)
        db.commit()

    return RedirectResponse(url="/admin/projects/", status_code=303)
