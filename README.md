#Narrate AI – Interactive Storyboard Prototype

Convert your book or story into a cinematic storyboard.

Narrate AI is a full-stack prototype that transforms narrative text into interactive visual scenes. Designed for writers and storytellers, it provides a “movie-like” experience for your story without heavy AI infrastructure.

Features

Upload text or PDF: Automatically splits content into individual scenes.

Interactive scene preview: Navigate with play, next, previous, and regenerate controls.

SVG-based visualization: Placeholder images simulate the animation of your story.

Expandable architecture: Easily integrate AI-generated images or video in the future.

Frontend: React + TypeScript with Vite

Backend: FastAPI + Python, using MongoDB/local storage

Demo

Include GIFs or screenshots showing scene navigation with SVG placeholders.

Installation (Local Prototype)
# Clone the repo
git clone (https://github.com/Sarthak12397/Narrate_AI/)
cd narrate-ai

# Backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm run dev

Usage

Upload your text or PDF.

View scenes with placeholder visuals.

Navigate through your story with the cinematic controls.

Vision

This prototype demonstrates the potential of AI-powered storytelling. Future iterations will replace SVG placeholders with AI-generated images or video, creating a fully immersive animated experience from text.
