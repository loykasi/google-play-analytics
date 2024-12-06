from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.dialects.mysql import insert
from ...database.database import get_db
from ...database.models import Categories

router = APIRouter()

@router.get("/categories", tags=["database"])
async def get(db: Session = Depends(get_db)):
    return db.query(Categories).limit(5).all()


@router.post("/categories", tags=["database"])
async def post(data: List[dict] = [], db: Session = Depends(get_db)):
    stmt = insert(Categories).values(data)
    stmt = stmt.on_duplicate_key_update(
        name=stmt.inserted.name
    )
    db.execute(stmt)
    db.commit()
    return "OK"