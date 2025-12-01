# src/schemas.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectOut(ProjectCreate):
    id: str = Field(..., alias="_id")
    created_at: datetime

    class Config:
        validate_by_name = True  # Pydantic v2 change
        arbitrary_types_allowed = True

class SceneCreate(BaseModel):
    project_id: str
    title: str
    prompt: Optional[str] = None
    duration: Optional[float] = 3.0

class SceneOut(SceneCreate):
    id: str = Field(..., alias="_id")
    created_at: datetime

    class Config:
        validate_by_name = True
