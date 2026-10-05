"""
=========================================================
Main FastAPI Application
Project : AI Mental Health Chatbot (FYP)
=========================================================
"""

from fastapi import FastAPI

from app.api.chat_routes import router as chat_router

app = FastAPI(

    title="AI Mental Health Chatbot API",

    description="Backend API for Emotion, Stress and Depression Detection",

    version="1.0.0"

)

# -------------------------------------------------------
# Root Endpoint
# -------------------------------------------------------

@app.get("/")
def home():

    return {
        "message": "AI Mental Health Chatbot Backend Running Successfully!"
    }

# -------------------------------------------------------
# Register API Routes
# -------------------------------------------------------

app.include_router(chat_router)