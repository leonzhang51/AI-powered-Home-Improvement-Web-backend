"""
Service for integrating with AI agents system.
"""
import sys
import os
from pathlib import Path
import asyncio
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from datetime import datetime

# Add AI agents path to Python path
ai_agents_path = "/Users/liezhang/Desktop/github/AI-Agents-LangChain-LangGraph-LangSmith"
if ai_agents_path not in sys.path:
    sys.path.append(ai_agents_path)

from app.core.config import Settings
from app.crud.crud_agent_session import agent_session as crud_agent_session
from app.crud.crud_rendering import rendering as crud_rendering
from app.crud.crud_project_plan import project_plan as crud_project_plan
from app.crud.crud_shopping_list import shopping_list as crud_shopping_list
from app.schemas.schemas import (
    AgentSessionCreate,
    RenderingCreate,
    ProjectPlanCreate,
    ShoppingListCreate
)

# Import AI agents directly
try:
    from graphs.diy_workflow import DIYWorkflow
    from utils.helpers import generate_session_id
    AI_AGENTS_AVAILABLE = True
except ImportError as e:
    print(f"Warning: AI agents not available: {e}")
    AI_AGENTS_AVAILABLE = False

settings = Settings()


class AIAgentsService:
    """Service for communicating with the AI agents system."""

    def __init__(self):
        self.base_url = settings.agents_service_url
        self.timeout = settings.agents_service_timeout
        self.workflow = None

    def _get_workflow(self):
        """Get or create workflow instance."""
        if not AI_AGENTS_AVAILABLE:
            raise Exception("AI agents system is not available")

        if self.workflow is None:
            self.workflow = DIYWorkflow()
        return self.workflow
    
    async def process_project(
        self, 
        db: Session, 
        project_id: int,
        project_description: str,
        room_type: str,
        style_preference: str,
        budget_range: str,
        user_id: int
    ) -> Dict[str, Any]:
        """
        Process a DIY project through the AI agents workflow.
        
        This method:
        1. Creates an agent session
        2. Calls the AI agents service
        3. Processes the results and saves to database
        4. Returns the processed results
        """
        # Create agent session
        session_data = AgentSessionCreate(
            project_id=project_id,
            status="active",
            started_at=datetime.utcnow(),
            agent_outputs={}
        )
        session = crud_agent_session.create(db, obj_in=session_data)
        
        try:
            # Get workflow instance
            workflow = self._get_workflow()

            # Create user input from project description
            user_input = f"I want to renovate my {room_type} with {style_preference} style. {project_description}"
            if budget_range:
                user_input += f" My budget is {budget_range}."

            # Run the AI agents workflow directly
            result = workflow.run_workflow(
                user_input=user_input,
                image_description=None,
                session_id=generate_session_id()
            )

            # Convert result to expected format - use the full ProjectSession
            processed_result = result.model_dump()
            processed_result["status"] = "completed"

            # Process the results
            await self._process_agent_results(db, project_id, session.id, processed_result)
            
            # Mark session as completed
            crud_agent_session.complete_session(db, session_id=session.id)
            
            return {
                "status": "success",
                "session_id": session.id,
                "results": processed_result
            }
            
        except Exception as e:
            # Mark session as failed
            crud_agent_session.fail_session(
                db, 
                session_id=session.id, 
                error_message=str(e)
            )
            raise e
    
    async def _process_agent_results(
        self, 
        db: Session, 
        project_id: int, 
        session_id: int, 
        results: Dict[str, Any]
    ):
        """Process and save AI agents results to database."""
        
        # Save renderings
        if "renderings" in results:
            for rendering_data in results["renderings"]:
                rendering_create = RenderingCreate(
                    project_id=project_id,
                    prompt=rendering_data.get("prompt", ""),
                    style=rendering_data.get("style", ""),
                    image_url=rendering_data.get("image_url"),
                    description=rendering_data.get("description"),
                    lighting=rendering_data.get("lighting"),
                    color_scheme=rendering_data.get("color_scheme", []),
                    focal_points=rendering_data.get("focal_points", [])
                )
                crud_rendering.create(db, obj_in=rendering_create)
        
        # Save project plan
        if "project_plan" in results:
            plan_data = results["project_plan"]
            plan_create = ProjectPlanCreate(
                project_id=project_id,
                title=plan_data.get("title", ""),
                description=plan_data.get("description", ""),
                total_estimated_cost=plan_data.get("total_estimated_cost", 0.0),
                estimated_time=plan_data.get("estimated_time", ""),
                difficulty_level=plan_data.get("difficulty_level", "beginner"),
                materials=plan_data.get("materials", []),
                tools=plan_data.get("tools", []),
                preparation_steps=plan_data.get("preparation_steps", []),
                execution_steps=plan_data.get("execution_steps", []),
                safety_considerations=plan_data.get("safety_considerations", []),
                tips_and_tricks=plan_data.get("tips_and_tricks", [])
            )
            crud_project_plan.create(db, obj_in=plan_create)
        
        # Save shopping list
        if "shopping_list" in results:
            shopping_data = results["shopping_list"]
            shopping_create = ShoppingListCreate(
                project_id=project_id,
                items=shopping_data.get("items", []),
                total_cost=shopping_data.get("total_cost", 0.0),
                stores=shopping_data.get("stores", []),
                alternatives=shopping_data.get("alternatives", [])
            )
            crud_shopping_list.create(db, obj_in=shopping_create)
    
    async def generate_renderings(
        self,
        db: Session,
        project_id: int,
        style_preferences: List[str],
        additional_prompts: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """Generate additional renderings for a project."""

        try:
            # Get workflow instance
            workflow = self._get_workflow()

            # Create user input for additional renderings
            styles_text = ", ".join(style_preferences)
            user_input = f"Generate additional design renderings with {styles_text} styles."
            if additional_prompts:
                user_input += f" Additional requirements: {', '.join(additional_prompts)}"

            # Run workflow for additional renderings
            result = workflow.run_workflow(
                user_input=user_input,
                image_description=None,
                session_id=generate_session_id()
            )

            # Save new renderings to database
            renderings = []
            for img in result.generated_images:
                rendering_create = RenderingCreate(
                    project_id=project_id,
                    prompt=img.prompt if hasattr(img, 'prompt') else "",
                    style=img.style if hasattr(img, 'style') else styles_text,
                    image_url=img.image_url if hasattr(img, 'image_url') else None,
                    description=img.description if hasattr(img, 'description') else "",
                    lighting=img.lighting if hasattr(img, 'lighting') else None,
                    color_scheme=img.color_scheme if hasattr(img, 'color_scheme') else [],
                    focal_points=img.focal_points if hasattr(img, 'focal_points') else []
                )
                rendering_obj = crud_rendering.create(db, obj_in=rendering_create)
                renderings.append(rendering_obj)

            return renderings

        except Exception as e:
            print(f"Error generating renderings: {e}")
            return []
    
    async def regenerate_plan(
        self,
        db: Session,
        project_id: int,
        selected_rendering_ids: List[int],
        custom_requirements: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Regenerate project plan based on selected renderings."""

        try:
            # Get workflow instance
            workflow = self._get_workflow()

            # Get selected renderings info
            renderings = []
            for rendering_id in selected_rendering_ids:
                rendering = crud_rendering.get(db, id=rendering_id)
                if rendering:
                    renderings.append(rendering)

            # Create user input for plan regeneration
            user_input = "Generate a detailed project plan based on the selected design renderings."
            if custom_requirements:
                req_text = ", ".join([f"{k}: {v}" for k, v in custom_requirements.items()])
                user_input += f" Additional requirements: {req_text}"

            # Run workflow for plan generation
            result = workflow.run_workflow(
                user_input=user_input,
                image_description=None,
                session_id=generate_session_id()
            )

            # Update project plan in database
            result_data = result.model_dump()
            if result_data.get("decoration_plan"):
                plan_data = result_data["decoration_plan"]
                existing_plan = crud_project_plan.get_by_project(db, project_id=project_id)

                if existing_plan:
                    # Update existing plan
                    plan_update = {
                        "title": plan_data.get("title", "Updated Project Plan"),
                        "description": plan_data.get("description", ""),
                        "total_estimated_cost": plan_data.get("total_estimated_cost", 0.0),
                        "estimated_time": plan_data.get("estimated_time", ""),
                        "difficulty_level": plan_data.get("difficulty_level", "beginner"),
                        "materials": plan_data.get("materials", []),
                        "tools": plan_data.get("tools", []),
                        "preparation_steps": plan_data.get("preparation_steps", []),
                        "execution_steps": plan_data.get("execution_steps", []),
                        "safety_considerations": plan_data.get("safety_considerations", []),
                        "tips_and_tricks": plan_data.get("tips_and_tricks", [])
                    }
                    crud_project_plan.update(db, db_obj=existing_plan, obj_in=plan_update)

            return {
                "status": "success",
                "project_plan": result_data.get("decoration_plan")
            }

        except Exception as e:
            print(f"Error regenerating plan: {e}")
            return {"status": "error", "message": str(e)}


ai_agents_service = AIAgentsService()
