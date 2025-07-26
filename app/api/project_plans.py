"""
Project Plans API routes.
"""
from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.security import get_current_active_user
from app.crud.crud_project import project as crud_project
from app.crud.crud_project_plan import project_plan as crud_project_plan
from app.schemas.schemas import ProjectPlan, ProjectPlanUpdate, User

router = APIRouter()


@router.get("/project/{project_id}", response_model=ProjectPlan)
def read_project_plan(
    *,
    db: Session = Depends(get_db),
    project_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get project plan for a project.
    """
    project = crud_project.get(db, id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    project_plan = crud_project_plan.get_by_project(db, project_id=project_id)
    if not project_plan:
        raise HTTPException(status_code=404, detail="Project plan not found")
    
    return project_plan


@router.get("/{plan_id}", response_model=ProjectPlan)
def read_plan(
    *,
    db: Session = Depends(get_db),
    plan_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get project plan by ID.
    """
    project_plan = crud_project_plan.get(db, id=plan_id)
    if not project_plan:
        raise HTTPException(status_code=404, detail="Project plan not found")
    
    # Check if user owns the project this plan belongs to
    project = crud_project.get(db, id=project_plan.project_id)
    if not project or project.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return project_plan


@router.put("/{plan_id}", response_model=ProjectPlan)
def update_project_plan(
    *,
    db: Session = Depends(get_db),
    plan_id: int,
    plan_in: ProjectPlanUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update project plan.
    """
    project_plan = crud_project_plan.get(db, id=plan_id)
    if not project_plan:
        raise HTTPException(status_code=404, detail="Project plan not found")
    
    # Check if user owns the project this plan belongs to
    project = crud_project.get(db, id=project_plan.project_id)
    if not project or project.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    project_plan = crud_project_plan.update(db, db_obj=project_plan, obj_in=plan_in)
    return project_plan


@router.delete("/{plan_id}")
def delete_project_plan(
    *,
    db: Session = Depends(get_db),
    plan_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Delete project plan.
    """
    project_plan = crud_project_plan.get(db, id=plan_id)
    if not project_plan:
        raise HTTPException(status_code=404, detail="Project plan not found")
    
    # Check if user owns the project this plan belongs to
    project = crud_project.get(db, id=project_plan.project_id)
    if not project or project.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    project_plan = crud_project_plan.remove(db, id=plan_id)
    return {"message": "Project plan deleted successfully"}
