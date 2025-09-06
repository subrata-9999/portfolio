from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# Import your routers
from app.routes import admin_auth, admin_hero, admin_about, admin_skill, admin_project, admin_edu, admin_link

app = FastAPI(title="Portfolio Admin")

# -----------------------------
# CORS (for frontend JS if needed)
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Mount static folder
# -----------------------------
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
# -----------------------------
# Include Routers
# -----------------------------
app.include_router(admin_auth.router)
app.include_router(admin_hero.router)
app.include_router(admin_about.router)
app.include_router(admin_skill.router)
app.include_router(admin_project.router)
app.include_router(admin_edu.router)
app.include_router(admin_link.router)


# -----------------------------
# Root endpoint (optional)
# -----------------------------
@app.get("/")
def root():
    return {"message": "Welcome to Portfolio FastAPI"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000))
    )


# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/")
# def root():
#     return {"message": "Hello FastAPI is working!"}
