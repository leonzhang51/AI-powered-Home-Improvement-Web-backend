"""
AI Agents API routes for direct interaction with agents system.
"""
from typing import Any, List, Optional, Dict
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.security import get_current_active_user
from app.crud.crud_project import project as crud_project
from app.schemas.schemas import User
from app.services.ai_agents_service import ai_agents_service

router = APIRouter()


@router.post("/process-project/{project_id}")
async def process_project(
    *,
    db: Session = Depends(get_db),
    project_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Process an existing project through the AI agents workflow.
    """
    project = crud_project.get(db, id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    try:
        result = await ai_agents_service.process_project(
            db=db,
            project_id=project_id,
            project_description=project.description,
            room_type=project.room_type,
            style_preference=project.style_preference,
            budget_range=project.budget_range,
            user_id=current_user.id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI processing failed: {str(e)}")


@router.post("/generate-renderings/{project_id}")
async def generate_additional_renderings(
    *,
    db: Session = Depends(get_db),
    project_id: int,
    style_preferences: List[str] = Query(...),
    additional_prompts: Optional[List[str]] = Query(None),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Generate additional renderings for a project.
    """
    project = crud_project.get(db, id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    try:
        renderings = await ai_agents_service.generate_renderings(
            db=db,
            project_id=project_id,
            style_preferences=style_preferences,
            additional_prompts=additional_prompts
        )
        return {"renderings": renderings, "count": len(renderings)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Rendering generation failed: {str(e)}")


@router.post("/regenerate-plan/{project_id}")
async def regenerate_project_plan(
    *,
    db: Session = Depends(get_db),
    project_id: int,
    selected_rendering_ids: List[int] = Query(...),
    custom_requirements: Optional[Dict[str, Any]] = None,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Regenerate project plan based on selected renderings.
    """
    project = crud_project.get(db, id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    try:
        result = await ai_agents_service.regenerate_plan(
            db=db,
            project_id=project_id,
            selected_rendering_ids=selected_rendering_ids,
            custom_requirements=custom_requirements
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Plan regeneration failed: {str(e)}")


@router.get("/status/{project_id}")
def get_agent_processing_status(
    *,
    db: Session = Depends(get_db),
    project_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get the status of AI agent processing for a project.
    """
    from app.crud.crud_agent_session import agent_session as crud_agent_session
    
    project = crud_project.get(db, id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Get the most recent active session
    active_session = crud_agent_session.get_active_session(db, project_id=project_id)
    all_sessions = crud_agent_session.get_by_project(db, project_id=project_id)
    
    return {
        "project_id": project_id,
        "active_session": active_session,
        "total_sessions": len(all_sessions),
        "latest_sessions": all_sessions[:5] if len(all_sessions) > 5 else all_sessions
    }
