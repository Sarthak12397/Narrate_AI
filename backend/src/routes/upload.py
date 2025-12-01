# src/routes/upload.py
import os
import uuid
from datetime import datetime
from fastapi import APIRouter, UploadFile, File, Form, BackgroundTasks, HTTPException
from PyPDF2 import PdfReader

from ..utils_image import generate_image
from ..db import db

router = APIRouter(prefix="/upload", tags=["upload"])
UPLOAD_FOLDER = "./uploads"

async def generate_scenes(story_text: str, job_id: str):
    """
    Split the story into paragraphs and generate an image for each paragraph.
    This keeps everything local and free by using your local Ollama image model.
    """
    # Split by blank lines into paragraphs
    paragraphs = [p.strip() for p in story_text.split("\n\n") if p.strip()]
    scene_docs = []

    for i, paragraph in enumerate(paragraphs, start=1):
        title = f"Scene {i}"
        description = paragraph
        image_prompt = paragraph  # generate image directly from the paragraph text

        # Try to generate an image for each scene
        image_url = ""
        try:
            # Generate a tiny SVG placeholder as a data: URL (no files, no static serving).
            image_url = await generate_image(image_prompt, None)
        except Exception as e:
            print("Image generation failed:", e)
            image_url = ""

        scene_docs.append({
            "scene_number": i,
            "title": title,
            "narration": description or title,
            "image_url": image_url,
            "job_id": job_id,
            "created_at": datetime.utcnow(),
        })

    if scene_docs:
        await db.scenes.insert_many(scene_docs)
        await db.render_jobs.update_one(
            {"job_id": job_id},
            {"$set": {"status": "done", "scene_count": len(scene_docs), "completed_at": datetime.utcnow()}}
        )
    else:
        await db.render_jobs.update_one(
            {"job_id": job_id},
            {"$set": {"status": "failed", "error": "Story text did not contain any scenes"}}
        )


@router.post("/file")
async def upload_file(
    background_tasks: BackgroundTasks,
    file: UploadFile | None = File(default=None),
    text: str | None = Form(default=None),
):
    # Read PDF or text
    story_text = ""
    filename = None
    if file:
        filename = file.filename
        if file.filename.lower().endswith(".pdf"):
            file.file.seek(0)
            pdf_reader = PdfReader(file.file)
            contents = []
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    contents.append(page_text.strip())
            story_text = "\n\n".join(contents)
        else:
            story_text = (await file.read()).decode("utf-8").strip()
    elif text:
        story_text = text.strip()

    if not story_text:
        raise HTTPException(status_code=400, detail="No story content provided")

    # Create a new job in DB
    job_id = str(uuid.uuid4())
    await db.render_jobs.insert_one({
        "job_id": job_id,
        "filename": filename or "text-upload",
        "status": "queued",
        "created_at": datetime.utcnow(),
        "text_length": len(story_text),
    })

    # Run scene generation in background
    background_tasks.add_task(generate_scenes, story_text, job_id)

    return {"job_id": job_id, "status": "queued"}


@router.get("/jobs/{job_id}")
async def get_job(job_id: str):
    job = await db.render_jobs.find_one({"job_id": job_id})
    if not job:
        raise HTTPException(404, "Job not found")
    job["_id"] = str(job["_id"])
    return job
