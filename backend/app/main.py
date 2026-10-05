"""
Thathvamasi HR Consultancy - FastAPI Backend
Main application file
"""

import os
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import routes
from app.api import candidates, clients, blogs, auth, upload, contact
from app.core.config import settings
from app.core.database import init_db, close_db
from app.core.security import setup_security
from app.middleware.error_handler import ErrorHandlerMiddleware, RequestValidationMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events
    """
    # Setup logging
    from app.core.logging_config import setup_logging
    setup_logging()
    
    import logging
    logger = logging.getLogger(__name__)
    
    # Startup
    logger.info("🚀 Starting Thathvamasi HR Consultancy Backend...")
    logger.info(f"📊 Environment: {settings.ENVIRONMENT}")
    logger.info(f"🐘 Database: {settings.POSTGRES_DB}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}")
    
    # Initialize database connection and create tables
    try:
        await init_db()
        logger.info("✅ Database initialized successfully")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}", exc_info=True)
        raise
    
    # Create upload directories if they don't exist
    os.makedirs("app/static/uploads/resumes", exist_ok=True)
    os.makedirs("app/static/uploads/jds", exist_ok=True)
    os.makedirs("app/static/uploads/blog_images", exist_ok=True)
    logger.info("📁 Upload directories created")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down Thathvamasi HR Consultancy Backend...")
    await close_db()

# Create FastAPI application
app = FastAPI(
    title="Thathvamasi HR Consultancy API",
    description="Backend API for Thathvamasi HR Consultancy website",
    version="1.0.0",
    contact={
        "name": "Thathvamasi HR Consultancy",
        "url": "https://thathvamasi.com",
        "email": "contact@thathvamasi.com",
    },
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup security middleware
setup_security(app)

# Add custom middleware
app.add_middleware(ErrorHandlerMiddleware, debug=settings.ENVIRONMENT != "production")
app.add_middleware(RequestValidationMiddleware)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include API routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(candidates.router, prefix="/api/candidates", tags=["Candidates"])
app.include_router(clients.router, prefix="/api/clients", tags=["Clients"])
app.include_router(blogs.router, prefix="/api/blogs", tags=["Blogs"])
app.include_router(upload.router, prefix="/api/upload", tags=["Upload"])
app.include_router(contact.router, prefix="/api/contact", tags=["Contact"])

@app.get("/")
async def root():
    """
    Root endpoint - API status
    """
    return {
        "message": "Welcome to Thathvamasi HR Consultancy API",
        "version": "1.0.0",
        "status": "operational",
        "environment": settings.ENVIRONMENT,
        "database": "PostgreSQL",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    from datetime import datetime
    from app.core.database import engine
    
    try:
        # Test database connection
        async with engine.begin() as conn:
            from sqlalchemy import text
            await conn.execute(text("SELECT 1"))
        
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "database": "connected",
            "environment": settings.ENVIRONMENT
        }
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Service unhealthy: Database connection failed - {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )