"""
Dependency functions for API routes.
"""
from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.security import verify_token, get_current_user, get_current_active_user
from app.db.database import SessionLocal

security = HTTPBearer()


def get_db() -> Generator:
    """Get database session."""
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# Export the security dependencies
__all__ = ["get_db", "get_current_user", "get_current_active_user"]
