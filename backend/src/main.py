# src/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

# Import routers
from src.routes import projects, scenes, upload  # make sure 'upload' is here

app = FastAPI()

# Enable CORS for your frontend during dev (any localhost port)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # safe for local dev, simplifies port changes
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files for generated images
generated_dir = os.path.join(os.path.dirname(__file__), "..", "generated_images")
os.makedirs(generated_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=generated_dir), name="static")

# Include routers
app.include_router(projects.router)
app.include_router(scenes.router)
app.include_router(upload.router)  # ✅ this is critical

