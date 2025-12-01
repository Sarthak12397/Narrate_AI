# src/routes/projects.py
from fastapi import APIRouter, HTTPException
from ..db import db
from ..schemas import ProjectCreate, ProjectOut
from ..models import now, to_camel_id
from bson import ObjectId

router = APIRouter(prefix="/projects", tags=["projects"])

@router.post("", response_model=ProjectOut)
async def create_project(payload: ProjectCreate):
    doc = payload.dict()
    doc["created_at"] = now()
    res = await db.projects.insert_one(doc)
    created = await db.projects.find_one({"_id": res.inserted_id})
    return to_camel_id(created)

@router.get("/{project_id}", response_model=ProjectOut)
async def get_project(project_id: str):
    if not ObjectId.is_valid(project_id):
        raise HTTPException(400, "Invalid id")
    doc = await db.projects.find_one({"_id": ObjectId(project_id)})
    if not doc:
        raise HTTPException(404, "Not found")
    return to_camel_id(doc)

@router.get("", response_model=list[ProjectOut])
async def list_projects():
    cursor = db.projects.find().sort("created_at", 1)
    out = []
    async for d in cursor:
        out.append(to_camel_id(d))
    return out
