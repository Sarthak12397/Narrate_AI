# src/db.py
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME")
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")

# Async MongoDB client
client = AsyncIOMotorClient(MONGODB_URI)
Narrate = client[DB_NAME]

# Collections
Narrate.projects = Narrate["projects"]
Narrate.scenes = Narrate["scenes"]
Narrate.uploads = Narrate["uploads"]
Narrate.render_jobs = Narrate["render_jobs"]

db = Narrate  # for easy import
