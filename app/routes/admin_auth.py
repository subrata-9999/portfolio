from fastapi import APIRouter, Depends, Request, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import text
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from dotenv import load_dotenv
import os

from app.db import get_db
from app.models import Admin
from app.auth import verify_password, create_access_token, get_current_admin

# -----------------------------
# Load env variables
# -----------------------------
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

# -----------------------------
# Router and Templates
# -----------------------------
router = APIRouter(prefix="/admin", tags=["admin"])
templates = Jinja2Templates(directory="templates")

# -----------------------------
# Login Page (HTML)
# -----------------------------
@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


# -----------------------------
# Login API (Form data)
# -----------------------------

@router.post("/login")
def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.username == username).first()
    if not admin or not verify_password(password, admin.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": admin.username})

    response = RedirectResponse(url="/admin/dashboard", status_code=303)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=60*60,   # 1 hour
        path="/"         # 👈 cookie valid for all routes
    )
    return response


# -----------------------------
# Dashboard Page (Protected)
# -----------------------------
@router.get("/dashboard", response_class=HTMLResponse)
def dashboard_page(
    request: Request,
    current_admin=Depends(get_current_admin)
):
    return templates.TemplateResponse(
        "admin_dashboard.html",
        {"request": request, "admin": current_admin}
    )



# -----------------------------
# Logout API
# -----------------------------
@router.get("/logout")
def logout():
    response = RedirectResponse(url="/admin/login", status_code=303)
    response.delete_cookie("access_token", path="/")
    return response

# -----------------------------
# /me endpoint (optional JSON check)
# -----------------------------
@router.get("/me")
def get_admin_me(current_admin=Depends(get_current_admin)):
    return {"id": current_admin.id, "username": current_admin.username}


@router.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "DB connected"}
    except Exception as e:
        return {"error": str(e)}