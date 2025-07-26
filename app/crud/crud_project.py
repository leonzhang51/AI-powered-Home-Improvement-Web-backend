"""
CRUD operations for Project model.
"""
from typing import List
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.models import Project
from app.schemas.schemas import ProjectCreate, ProjectUpdate


class CRUDProject(CRUDBase[Project, ProjectCreate, ProjectUpdate]):
    def get_by_user(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Project]:
        return (
            db.query(self.model)
            .filter(Project.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_status(
        self, db: Session, *, status: str, skip: int = 0, limit: int = 100
    ) -> List[Project]:
        return (
            db.query(self.model)
            .filter(Project.status == status)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_user_projects_by_status(
        self, db: Session, *, user_id: int, status: str
    ) -> List[Project]:
        return (
            db.query(self.model)
            .filter(Project.user_id == user_id, Project.status == status)
            .all()
        )


project = CRUDProject(Project)
