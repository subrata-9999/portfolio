from typing import Optional
from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Education, SkillStatus
from fastapi.templating import Jinja2Templates
from app.auth import get_current_admin

router = APIRouter(prefix="/admin/edu", tags=["Admin Education"])
templates = Jinja2Templates(directory="templates")

# Show education list
@router.get("/", response_class=HTMLResponse)
def show_edu(request: Request, db: Session = Depends(get_db), current_admin: str = Depends(get_current_admin)):
    edu_list = db.query(Education).all()
    return templates.TemplateResponse("admin_edu.html", {"request": request, "edu_list": edu_list})

# Add/Update education
@router.post("/save")
def save_edu(
    request: Request,
    db: Session = Depends(get_db),
    current_admin: str = Depends(get_current_admin),
    id: Optional[int] = Form(None),   # ✅ Use Optional here
    heading: str = Form(...),
    institute_string: str = Form(...),
    des_string: str = Form(...),
    score_string: str = Form(...),
    institute_link: str = Form(...),
    year_string: str = Form(...),
    status: str = Form("a")
):
    if id:  # update
        edu = db.query(Education).filter(Education.id == id).first()
        if edu:
            edu.heading = heading
            edu.institute_string = institute_string
            edu.des_string = des_string
            edu.score_string = score_string
            edu.institute_link = institute_link
            edu.year_string = year_string
            edu.status = SkillStatus(status)
            db.commit()
    else:  # add new
        new_edu = Education(
            heading=heading,
            institute_string=institute_string,
            des_string=des_string,
            score_string=score_string,
            institute_link=institute_link,
            year_string=year_string,
            status=SkillStatus(status)
        )
        db.add(new_edu)
        db.commit()

    return RedirectResponse(url="/admin/edu/", status_code=303)
