"""
Shopping Lists API routes.
"""
from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.security import get_current_active_user
from app.crud.crud_project import project as crud_project
from app.crud.crud_shopping_list import shopping_list as crud_shopping_list
from app.schemas.schemas import ShoppingList, ShoppingListUpdate, User

router = APIRouter()


@router.get("/project/{project_id}", response_model=ShoppingList)
def read_shopping_list(
    *,
    db: Session = Depends(get_db),
    project_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get shopping list for a project.
    """
    project = crud_project.get(db, id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    shopping_list = crud_shopping_list.get_by_project(db, project_id=project_id)
    if not shopping_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")
    
    return shopping_list


@router.get("/{list_id}", response_model=ShoppingList)
def read_list(
    *,
    db: Session = Depends(get_db),
    list_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get shopping list by ID.
    """
    shopping_list = crud_shopping_list.get(db, id=list_id)
    if not shopping_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")
    
    # Check if user owns the project this list belongs to
    project = crud_project.get(db, id=shopping_list.project_id)
    if not project or project.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return shopping_list


@router.put("/{list_id}", response_model=ShoppingList)
def update_shopping_list(
    *,
    db: Session = Depends(get_db),
    list_id: int,
    list_in: ShoppingListUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update shopping list.
    """
    shopping_list = crud_shopping_list.get(db, id=list_id)
    if not shopping_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")
    
    # Check if user owns the project this list belongs to
    project = crud_project.get(db, id=shopping_list.project_id)
    if not project or project.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    shopping_list = crud_shopping_list.update(db, db_obj=shopping_list, obj_in=list_in)
    return shopping_list


@router.delete("/{list_id}")
def delete_shopping_list(
    *,
    db: Session = Depends(get_db),
    list_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Delete shopping list.
    """
    shopping_list = crud_shopping_list.get(db, id=list_id)
    if not shopping_list:
        raise HTTPException(status_code=404, detail="Shopping list not found")
    
    # Check if user owns the project this list belongs to
    project = crud_project.get(db, id=shopping_list.project_id)
    if not project or project.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    shopping_list = crud_shopping_list.remove(db, id=list_id)
    return {"message": "Shopping list deleted successfully"}
