"""
Project service for handling complex project operations.
"""
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session

from app.crud.crud_project import project as crud_project
from app.crud.crud_rendering import rendering as crud_rendering
from app.crud.crud_project_plan import project_plan as crud_project_plan
from app.crud.crud_shopping_list import shopping_list as crud_shopping_list
from app.services.ai_agents_service import ai_agents_service
from app.schemas.schemas import ProjectCreate, ProjectUpdate


class ProjectService:
    """Service for handling project-related business logic."""
    
    async def create_project_with_ai_processing(
        self,
        db: Session,
        project_data: ProjectCreate,
        user_id: int,
        auto_process: bool = True
    ) -> Dict[str, Any]:
        """Create a new project and optionally process it with AI agents."""
        
        # Create the project
        project_create_data = project_data.dict()
        project_create_data["user_id"] = user_id
        project = crud_project.create(db, obj_in=project_create_data)
        
        # Convert SQLAlchemy model to dict for serialization
        project_dict = {
            "id": project.id,
            "title": project.title,
            "description": project.description,
            "room_type": project.room_type,
            "style_preference": project.style_preference,
            "budget_range": project.budget_range,
            "status": project.status,
            "user_id": project.user_id,
            "created_at": project.created_at,
            "updated_at": project.updated_at
        }
        
        result = {
            "project": project_dict,
            "ai_processing": None
        }
        
        # Automatically process with AI agents if requested
        if auto_process:
            try:
                ai_result = await ai_agents_service.process_project(
                    db=db,
                    project_id=project.id,
                    project_description=project.description,
                    room_type=project.room_type,
                    style_preference=project.style_preference,
                    budget_range=project.budget_range,
                    user_id=user_id
                )
                result["ai_processing"] = ai_result
                
                # Update project status
                crud_project.update(
                    db, 
                    db_obj=project, 
                    obj_in={"status": "in_progress"}
                )
                
            except Exception as e:
                # If AI processing fails, keep project in draft status
                result["ai_processing"] = {
                    "status": "failed",
                    "error": str(e)
                }
        
        return result
    
    def get_project_summary(self, db: Session, project_id: int) -> Dict[str, Any]:
        """Get a comprehensive summary of a project."""
        
        project = crud_project.get(db, id=project_id)
        if not project:
            return None
        
        # Get all related data
        renderings = crud_rendering.get_by_project(db, project_id=project_id)
        selected_renderings = crud_rendering.get_selected_by_project(db, project_id=project_id)
        project_plan = crud_project_plan.get_by_project(db, project_id=project_id)
        shopping_list = crud_shopping_list.get_by_project(db, project_id=project_id)
        
        return {
            "project": project,
            "renderings": {
                "total": len(renderings),
                "selected": len(selected_renderings),
                "all_renderings": renderings,
                "selected_renderings": selected_renderings
            },
            "project_plan": project_plan,
            "shopping_list": shopping_list,
            "completion_status": {
                "has_renderings": len(renderings) > 0,
                "has_selected_renderings": len(selected_renderings) > 0,
                "has_plan": project_plan is not None,
                "has_shopping_list": shopping_list is not None
            }
        }
    
    async def regenerate_project_components(
        self,
        db: Session,
        project_id: int,
        regenerate_renderings: bool = False,
        regenerate_plan: bool = False,
        regenerate_shopping: bool = False,
        style_preferences: Optional[List[str]] = None,
        custom_requirements: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Regenerate specific components of a project."""
        
        results = {}
        
        if regenerate_renderings and style_preferences:
            try:
                new_renderings = await ai_agents_service.generate_renderings(
                    db=db,
                    project_id=project_id,
                    style_preferences=style_preferences
                )
                results["new_renderings"] = new_renderings
            except Exception as e:
                results["rendering_error"] = str(e)
        
        if regenerate_plan:
            try:
                # Get selected renderings
                selected_renderings = crud_rendering.get_selected_by_project(
                    db, project_id=project_id
                )
                selected_ids = [r.id for r in selected_renderings]
                
                updated_plan = await ai_agents_service.regenerate_plan(
                    db=db,
                    project_id=project_id,
                    selected_rendering_ids=selected_ids,
                    custom_requirements=custom_requirements
                )
                results["updated_plan"] = updated_plan
            except Exception as e:
                results["plan_error"] = str(e)
        
        return results
    
    def get_user_project_stats(self, db: Session, user_id: int) -> Dict[str, Any]:
        """Get statistics about user's projects."""
        
        all_projects = crud_project.get_by_user(db, user_id=user_id)
        
        stats = {
            "total_projects": len(all_projects),
            "by_status": {},
            "by_room_type": {},
            "by_style": {},
            "completion_rate": 0
        }
        
        for project in all_projects:
            # Count by status
            status = project.status
            stats["by_status"][status] = stats["by_status"].get(status, 0) + 1
            
            # Count by room type
            room_type = project.room_type
            stats["by_room_type"][room_type] = stats["by_room_type"].get(room_type, 0) + 1
            
            # Count by style
            style = project.style_preference
            stats["by_style"][style] = stats["by_style"].get(style, 0) + 1
        
        # Calculate completion rate
        completed = stats["by_status"].get("completed", 0)
        if stats["total_projects"] > 0:
            stats["completion_rate"] = (completed / stats["total_projects"]) * 100
        
        return stats


project_service = ProjectService()
