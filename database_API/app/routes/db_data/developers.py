from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.dialects.mysql import insert
from ...database.database import get_db
from ...database.models import Developers

router = APIRouter()

@router.get("/developers", tags=["database"])
async def get(db: Session = Depends(get_db)):
    return db.query(Developers).limit(5).all()


@router.post("/developers", tags=["database"])
async def post(data: List[dict] = [], db: Session = Depends(get_db)):
    stmt = insert(Developers).values(data)
    stmt = stmt.on_duplicate_key_update(
        developer = stmt.inserted.developer
    )
    db.execute(stmt)
    db.commit()
    return "OK"