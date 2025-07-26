"""
Users API routes.
"""
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.security import get_current_active_user
from app.crud.crud_user import user as crud_user
from app.schemas.schemas import User, UserUpdate
from app.services.project_service import project_service

router = APIRouter()


@router.get("/me", response_model=User)
def read_user_me(
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.put("/me", response_model=User)
def update_user_me(
    *,
    db: Session = Depends(get_db),
    password: str = None,
    full_name: str = None,
    email: str = None,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    current_user_data = {}
    if password is not None:
        current_user_data["password"] = password
    if full_name is not None:
        current_user_data["full_name"] = full_name
    if email is not None:
        current_user_data["email"] = email
    
    user = crud_user.update(db, db_obj=current_user, obj_in=current_user_data)
    return user


@router.get("/me/stats")
def read_user_stats(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get current user's project statistics.
    """
    stats = project_service.get_user_project_stats(db, user_id=current_user.id)
    return stats


@router.get("/{user_id}", response_model=User)
def read_user(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get a specific user by id (for admin use or public profiles).
    """
    user = crud_user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # For now, only allow users to see their own profile
    if user.id != current_user.id:
        raise HTTPException(
            status_code=403, 
            detail="Not enough permissions"
        )
    
    return user
