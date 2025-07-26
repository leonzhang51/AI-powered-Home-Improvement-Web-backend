"""
CRUD operations for ProjectPlan model.
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.models import ProjectPlan
from app.schemas.schemas import ProjectPlanCreate, ProjectPlanUpdate


class CRUDProjectPlan(CRUDBase[ProjectPlan, ProjectPlanCreate, ProjectPlanUpdate]):
    def get_by_project(self, db: Session, *, project_id: int) -> Optional[ProjectPlan]:
        return db.query(self.model).filter(ProjectPlan.project_id == project_id).first()

    def get_by_difficulty(
        self, db: Session, *, difficulty: str, skip: int = 0, limit: int = 100
    ) -> List[ProjectPlan]:
        return (
            db.query(self.model)
            .filter(ProjectPlan.difficulty_level == difficulty)
            .offset(skip)
            .limit(limit)
            .all()
        )


project_plan = CRUDProjectPlan(ProjectPlan)
