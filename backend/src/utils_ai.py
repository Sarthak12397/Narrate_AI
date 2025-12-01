# utils_ai.py
from ollama import Client

client = Client(host='http://localhost:11434')

async def generate_scenes_from_story(story_text: str) -> list:
    """
    Takes the uploaded story text and generates structured scenes.
    Uses local Ollama model (free).
    """

    prompt = f"""
    Break the following story into SCENES.

    For each SCENE return JSON EXACTLY like this:
    {{
        "scene_number": 1,
        "title": "string",
        "description": "string of what happens",
        "image_prompt": "string describing image"
    }}

    STORY:
    {story_text}
    """

    response = client.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
    raw = response["message"]["content"]

    # IMPORTANT: Try to parse output
    import json
    try:
        scenes = json.loads(raw)
    except:
        scenes = []

    return scenes
