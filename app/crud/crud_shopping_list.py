"""
CRUD operations for ShoppingList model.
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.models import ShoppingList
from app.schemas.schemas import ShoppingListCreate, ShoppingListUpdate


class CRUDShoppingList(CRUDBase[ShoppingList, ShoppingListCreate, ShoppingListUpdate]):
    def get_by_project(self, db: Session, *, project_id: int) -> Optional[ShoppingList]:
        return db.query(self.model).filter(ShoppingList.project_id == project_id).first()

    def get_by_budget_range(
        self, db: Session, *, min_cost: float, max_cost: float
    ) -> List[ShoppingList]:
        return (
            db.query(self.model)
            .filter(
                ShoppingList.total_cost >= min_cost,
                ShoppingList.total_cost <= max_cost
            )
            .all()
        )


shopping_list = CRUDShoppingList(ShoppingList)
