"""
FastAPI main application.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.core.config import Settings
from app.api import (
    auth_router,
    users_router,
    projects_router,
    renderings_router,
    project_plans_router,
    shopping_lists_router,
    ai_agents_router
)

settings = Settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="AI-powered Home DIY Improvement API",
    openapi_url="/api/v1/openapi.json" if settings.environment != "production" else None,
)

# Set all CORS enabled origins
if settings.cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.cors_origins],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Add trusted host middleware for security
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

# Include API routers
app.include_router(auth_router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(users_router, prefix="/api/v1/users", tags=["users"])
app.include_router(projects_router, prefix="/api/v1/projects", tags=["projects"])
app.include_router(renderings_router, prefix="/api/v1/renderings", tags=["renderings"])
app.include_router(project_plans_router, prefix="/api/v1/project-plans", tags=["project-plans"])
app.include_router(shopping_lists_router, prefix="/api/v1/shopping-lists", tags=["shopping-lists"])
app.include_router(ai_agents_router, prefix="/api/v1/ai-agents", tags=["ai-agents"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "AI-powered Home DIY Improvement API",
        "version": settings.version,
        "docs_url": "/docs" if settings.environment != "production" else None
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "environment": settings.environment}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8000,
        reload=settings.debug,
        log_level="debug" if settings.debug else "info"
    )
