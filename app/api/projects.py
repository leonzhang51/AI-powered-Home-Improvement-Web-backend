"""
Projects API routes.
"""
from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.security import get_current_active_user
from app.crud.crud_project import project as crud_project
from app.schemas.schemas import (
    Project, ProjectCreate, ProjectUpdate, User, ProjectStatus
)
from app.services.project_service import project_service

router = APIRouter()


@router.get("/", response_model=List[Project])
def read_projects(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    status: Optional[ProjectStatus] = None,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve user's projects.
    """
    if status:
        projects = crud_project.get_user_projects_by_status(
            db, user_id=current_user.id, status=status.value
        )
    else:
        projects = crud_project.get_by_user(
            db, user_id=current_user.id, skip=skip, limit=limit
        )
    return projects


@router.post("/", response_model=dict)
async def create_project(
    *,
    db: Session = Depends(get_db),
    project_in: ProjectCreate,
    auto_process: bool = Query(True, description="Automatically process with AI agents"),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create new project and optionally process with AI agents.
    """
    result = await project_service.create_project_with_ai_processing(
        db=db,
        project_data=project_in,
        user_id=current_user.id,
        auto_process=auto_process
    )
    return result


@router.get("/{project_id}", response_model=Project)
def read_project(
    *,
    db: Session = Depends(get_db),
    project_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get project by ID.
    """
    project = crud_project.get(db, id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return project


@router.get("/{project_id}/summary")
def read_project_summary(
    *,
    db: Session = Depends(get_db),
    project_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get comprehensive project summary with all related data.
    """
    project = crud_project.get(db, id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    summary = project_service.get_project_summary(db, project_id=project_id)
    return summary


@router.put("/{project_id}", response_model=Project)
def update_project(
    *,
    db: Session = Depends(get_db),
    project_id: int,
    project_in: ProjectUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update project.
    """
    project = crud_project.get(db, id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    project = crud_project.update(db, db_obj=project, obj_in=project_in)
    return project


@router.delete("/{project_id}")
def delete_project(
    *,
    db: Session = Depends(get_db),
    project_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Delete project.
    """
    project = crud_project.get(db, id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    project = crud_project.remove(db, id=project_id)
    return {"message": "Project deleted successfully"}


@router.post("/{project_id}/regenerate")
async def regenerate_project_components(
    *,
    db: Session = Depends(get_db),
    project_id: int,
    regenerate_renderings: bool = Query(False),
    regenerate_plan: bool = Query(False),
    regenerate_shopping: bool = Query(False),
    style_preferences: Optional[List[str]] = Query(None),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Regenerate specific components of a project.
    """
    project = crud_project.get(db, id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    results = await project_service.regenerate_project_components(
        db=db,
        project_id=project_id,
        regenerate_renderings=regenerate_renderings,
        regenerate_plan=regenerate_plan,
        regenerate_shopping=regenerate_shopping,
        style_preferences=style_preferences
    )
    
    return results
