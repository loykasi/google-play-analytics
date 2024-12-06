from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.dialects.mysql import insert
from ...database.database import get_db
from ...database.models import App_Category

router = APIRouter()

@router.get("/app-category", tags=["database"])
async def get(db: Session = Depends(get_db)):
    return db.query(App_Category).limit(5).all()


@router.post("/app-category", tags=["database"])
async def post(data: List[dict] = [], db: Session = Depends(get_db)):
    stmt = insert(App_Category).values(data)
    stmt = stmt.on_duplicate_key_update(
        app_id=stmt.inserted.app_id,
        category_id=stmt.inserted.category_id
    )
    db.execute(stmt)
    db.commit()
    return "OK"