"""
API routes module.
"""
from .auth import router as auth_router
from .users import router as users_router
from .projects import router as projects_router
from .renderings import router as renderings_router
from .project_plans import router as project_plans_router
from .shopping_lists import router as shopping_lists_router
from .ai_agents import router as ai_agents_router

__all__ = [
    "auth_router",
    "users_router", 
    "projects_router",
    "renderings_router",
    "project_plans_router",
    "shopping_lists_router",
    "ai_agents_router"
]
