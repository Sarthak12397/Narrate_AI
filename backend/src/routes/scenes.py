from fastapi import APIRouter, HTTPException
from ..db import db
from ..models import to_camel_id
from bson import ObjectId

router = APIRouter(prefix="/scenes", tags=["scenes"])

@router.get("/by_project/{project_id}")
async def list_by_project(project_id: str):
    if not ObjectId.is_valid(project_id):
        raise HTTPException(400, "Invalid project id")
    cursor = db.scenes.find({"project_id": ObjectId(project_id)}).sort("created_at", 1)
    out = []
    async for d in cursor:
        d["project_id"] = str(d["project_id"])
        out.append(to_camel_id(d))
    return out


@router.get("/by_job/{job_id}")
async def list_by_job(job_id: str):
    cursor = db.scenes.find({"job_id": job_id}).sort("scene_number", 1)
    out = []
    async for d in cursor:
        out.append(to_camel_id(d))
    if not out:
        raise HTTPException(404, "No scenes for that job yet")
    return out