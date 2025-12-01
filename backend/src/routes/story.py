# routes/story.py
from fastapi import APIRouter, UploadFile, HTTPException
from utils_ai import generate_scenes_from_story
from utils_image import generate_image
from pymongo import MongoClient
import os

router = APIRouter()

mongo = MongoClient("mongodb://localhost:27017")
db = mongo["narrate_ai"]
projects = db["projects"]
scenes = db["scenes"]


@router.post("/upload_story/{project_id}")
async def upload_story(project_id: str, file: UploadFile):

    text = (await file.read()).decode("utf-8")

    # 1) AI: turn story → scenes
    generated_scenes = await generate_scenes_from_story(text)

    if not generated_scenes:
        raise HTTPException(status_code=500, detail="AI failed to generate scenes")

    final_scenes = []

    for sc in generated_scenes:
        img_path = f"generated_images/{project_id}_scene_{sc['scene_number']}.png"
        os.makedirs("generated_images", exist_ok=True)

        # 2) AI: generate image for each scene
        await generate_image(sc["image_prompt"], img_path)

        # 3) Save to DB
        record = {
            "project_id": project_id,
            "scene_number": sc["scene_number"],
            "title": sc["title"],
            "description": sc["description"],
            "image_path": img_path
        }

        scenes.insert_one(record)
        final_scenes.append(record)

    return {"status": "success", "scenes": final_scenes}
