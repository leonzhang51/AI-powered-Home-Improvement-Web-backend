"""
CRUD operations for Rendering model.
"""
from typing import List
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.models import Rendering
from app.schemas.schemas import RenderingCreate, RenderingUpdate


class CRUDRendering(CRUDBase[Rendering, RenderingCreate, RenderingUpdate]):
    def get_by_project(self, db: Session, *, project_id: int) -> List[Rendering]:
        return db.query(self.model).filter(Rendering.project_id == project_id).all()

    def get_selected_by_project(self, db: Session, *, project_id: int) -> List[Rendering]:
        return (
            db.query(self.model)
            .filter(Rendering.project_id == project_id, Rendering.is_selected == True)
            .all()
        )

    def mark_as_selected(self, db: Session, *, rendering_id: int) -> Rendering:
        db_obj = db.query(self.model).filter(Rendering.id == rendering_id).first()
        if db_obj:
            db_obj.is_selected = True
            db.commit()
            db.refresh(db_obj)
        return db_obj

    def unmark_as_selected(self, db: Session, *, rendering_id: int) -> Rendering:
        db_obj = db.query(self.model).filter(Rendering.id == rendering_id).first()
        if db_obj:
            db_obj.is_selected = False
            db.commit()
            db.refresh(db_obj)
        return db_obj


rendering = CRUDRendering(Rendering)
