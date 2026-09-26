"""
=========================================================
Main FastAPI Application
Project : AI Mental Health Chatbot (FYP)
=========================================================
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.chat_routes import router as chat_router
from app.api.auth_routes import router as auth_router
from app.api.mood_routes import router as mood_router
from app.api.journal_routes import router as journal_router
from app.api.application_routes import router as application_router
from app.database.connection import init_pool, close_pool

@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_pool()
    yield
    close_pool()


app = FastAPI(

    title="AI Mental Health Chatbot API",

    description="Backend API for Emotion, Stress and Depression Detection",

    version="2.0.0",
    lifespan=lifespan,

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(auth_router)
app.include_router(mood_router)
app.include_router(journal_router)
app.include_router(application_router)
