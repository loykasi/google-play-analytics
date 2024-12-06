from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.dialects.mysql import insert
from ...database.database import get_db
from ...database.models import Apps

router = APIRouter()

@router.get("/apps", tags=["database"])
async def get(db: Session = Depends(get_db)):
    return db.query(Apps).limit(5).all()


@router.post("/apps", tags=["database"])
async def post(data: List[dict] = [], db: Session = Depends(get_db)):
    stmt = insert(Apps).values(data)
    stmt = stmt.on_duplicate_key_update(
        developer_id=stmt.inserted.developer_id,
        released=stmt.inserted.released
    )
    db.execute(stmt)
    db.commit()
    return "OK"