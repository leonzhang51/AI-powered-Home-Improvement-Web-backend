"""
CRUD operations for AgentSession model.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from app.crud.base import CRUDBase
from app.models.models import AgentSession
from app.schemas.schemas import AgentSessionCreate, AgentSessionUpdate


class CRUDAgentSession(CRUDBase[AgentSession, AgentSessionCreate, AgentSessionUpdate]):
    def get_by_project(self, db: Session, *, project_id: int) -> List[AgentSession]:
        return db.query(self.model).filter(AgentSession.project_id == project_id).all()

    def get_active_session(self, db: Session, *, project_id: int) -> Optional[AgentSession]:
        return (
            db.query(self.model)
            .filter(
                AgentSession.project_id == project_id,
                AgentSession.status == "active"
            )
            .first()
        )

    def complete_session(self, db: Session, *, session_id: int) -> AgentSession:
        db_obj = db.query(self.model).filter(AgentSession.id == session_id).first()
        if db_obj:
            db_obj.status = "completed"
            db_obj.ended_at = datetime.utcnow()
            db.commit()
            db.refresh(db_obj)
        return db_obj

    def fail_session(self, db: Session, *, session_id: int, error_message: str) -> AgentSession:
        db_obj = db.query(self.model).filter(AgentSession.id == session_id).first()
        if db_obj:
            db_obj.status = "failed"
            db_obj.ended_at = datetime.utcnow()
            db_obj.error_message = error_message
            db.commit()
            db.refresh(db_obj)
        return db_obj


agent_session = CRUDAgentSession(AgentSession)
