from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.dialects.mysql import insert
from ...database.database import get_db
from ...database.models import Versions

router = APIRouter()

@router.get("/versions", tags=["database"])
async def get(db: Session = Depends(get_db)):
    return db.query(Versions).limit(5).all()

@router.post("/versions", tags=["database"])
async def post(data: List[dict] = [], db: Session = Depends(get_db)):
    stmt = insert(Versions).values(data)
    stmt = stmt.on_duplicate_key_update(
        app_id=stmt.inserted.app_id,
        updated=stmt.inserted.updated
    )
    db.execute(stmt)
    db.commit()
    return "OK"