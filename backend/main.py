# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from .core.config import settings
from .api.chat import router as chat_router

# Create FastAPI app
app = FastAPI(
    title=settings.app_name, 
    version=settings.app_version,
    description="AI-powered productivity coach for better time management"
)

# Add CORS middleware with specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000", 
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "file://",  # Allow local HTML files
        "*"  # Allow all origins for development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint with basic app info"""
    return {
        "message": "🚀 Timely AI Coach API",
        "version": settings.app_version,
        "status": "running",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "app": settings.app_name,
        "version": settings.app_version,
        "openai_configured": bool(settings.openai_api_key),
        "database": settings.database_url.split("://")[0]
    }

@app.get("/config")
async def config_check():
    """Configuration check (for debugging)"""
    return {
        "app_name": settings.app_name,
        "debug_mode": settings.debug,
        "has_openai_key": bool(settings.openai_api_key),
        "has_anthropic_key": bool(settings.anthropic_api_key),
        "embedding_model": settings.embedding_model,
        "chroma_db_path": settings.chroma_db_path
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    print(f"Starting {settings.app_name} v{settings.app_version}")
    print(f"Debug mode: {settings.debug}")
    print(f"OpenAI key configured: {bool(settings.openai_api_key)}")
    print(f"CORS enabled for frontend connections")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    print(f"Shutting down {settings.app_name}")

# Include API routers
app.include_router(chat_router, prefix="/api/v1")