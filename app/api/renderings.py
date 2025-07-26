"""
Renderings API routes.
"""
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.security import get_current_active_user
from app.crud.crud_project import project as crud_project
from app.crud.crud_rendering import rendering as crud_rendering
from app.schemas.schemas import Rendering, RenderingUpdate, User

router = APIRouter()


@router.get("/project/{project_id}", response_model=List[Rendering])
def read_project_renderings(
    *,
    db: Session = Depends(get_db),
    project_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get all renderings for a project.
    """
    project = crud_project.get(db, id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    renderings = crud_rendering.get_by_project(db, project_id=project_id)
    return renderings


@router.get("/project/{project_id}/selected", response_model=List[Rendering])
def read_selected_renderings(
    *,
    db: Session = Depends(get_db),
    project_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get selected renderings for a project.
    """
    project = crud_project.get(db, id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    renderings = crud_rendering.get_selected_by_project(db, project_id=project_id)
    return renderings


@router.get("/{rendering_id}", response_model=Rendering)
def read_rendering(
    *,
    db: Session = Depends(get_db),
    rendering_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get rendering by ID.
    """
    rendering = crud_rendering.get(db, id=rendering_id)
    if not rendering:
        raise HTTPException(status_code=404, detail="Rendering not found")
    
    # Check if user owns the project this rendering belongs to
    project = crud_project.get(db, id=rendering.project_id)
    if not project or project.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return rendering


@router.put("/{rendering_id}", response_model=Rendering)
def update_rendering(
    *,
    db: Session = Depends(get_db),
    rendering_id: int,
    rendering_in: RenderingUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update rendering.
    """
    rendering = crud_rendering.get(db, id=rendering_id)
    if not rendering:
        raise HTTPException(status_code=404, detail="Rendering not found")
    
    # Check if user owns the project this rendering belongs to
    project = crud_project.get(db, id=rendering.project_id)
    if not project or project.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    rendering = crud_rendering.update(db, db_obj=rendering, obj_in=rendering_in)
    return rendering


@router.post("/{rendering_id}/select", response_model=Rendering)
def select_rendering(
    *,
    db: Session = Depends(get_db),
    rendering_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Mark rendering as selected.
    """
    rendering = crud_rendering.get(db, id=rendering_id)
    if not rendering:
        raise HTTPException(status_code=404, detail="Rendering not found")
    
    # Check if user owns the project this rendering belongs to
    project = crud_project.get(db, id=rendering.project_id)
    if not project or project.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    rendering = crud_rendering.mark_as_selected(db, rendering_id=rendering_id)
    return rendering


@router.post("/{rendering_id}/unselect", response_model=Rendering)
def unselect_rendering(
    *,
    db: Session = Depends(get_db),
    rendering_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Unmark rendering as selected.
    """
    rendering = crud_rendering.get(db, id=rendering_id)
    if not rendering:
        raise HTTPException(status_code=404, detail="Rendering not found")
    
    # Check if user owns the project this rendering belongs to
    project = crud_project.get(db, id=rendering.project_id)
    if not project or project.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    rendering = crud_rendering.unmark_as_selected(db, rendering_id=rendering_id)
    return rendering


@router.delete("/{rendering_id}")
def delete_rendering(
    *,
    db: Session = Depends(get_db),
    rendering_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Delete rendering.
    """
    rendering = crud_rendering.get(db, id=rendering_id)
    if not rendering:
        raise HTTPException(status_code=404, detail="Rendering not found")
    
    # Check if user owns the project this rendering belongs to
    project = crud_project.get(db, id=rendering.project_id)
    if not project or project.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    rendering = crud_rendering.remove(db, id=rendering_id)
    return {"message": "Rendering deleted successfully"}
