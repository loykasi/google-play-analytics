from fastapi import APIRouter, Depends, Response
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.dialects.mysql import insert
from ...database.database import get_db
from ...database.models import ClusteringWeeks, ClusteringCategory, ClusteringDays
import pandas as pd
import json

router = APIRouter()

@router.get("/clustering/weeks", tags=["page 4"])
async def get_clustering_weeks(db: Session = Depends(get_db)):
    query = (
        db.query(
            ClusteringWeeks.clustering_data,
        )
    )

    df = pd.read_sql(query.statement, db.bind)
    df["clustering_data"] = df["clustering_data"].apply(json.loads)
    
    return df["clustering_data"].iloc[0]

@router.post("/clustering/weeks", tags=["database"])
async def post_clustering_weeks(data: List[dict] = [], db: Session = Depends(get_db)):
    stmt = insert(ClusteringWeeks).values(data)
    stmt = stmt.on_duplicate_key_update(
        clustering_data=stmt.inserted.clustering_data,
    )
    db.execute(stmt)
    db.commit()
    return "OK"

@router.get("/clustering/category", tags=["page 6"])
async def get_clustering_category(db: Session = Depends(get_db)):
    query = (
        db.query(
            ClusteringCategory.clustering_data,
        )
    )

    df = pd.read_sql(query.statement, db.bind)
    # df["clustering_data"] = df["clustering_data"].apply(json.loads)
    
    return df["clustering_data"].iloc[0]

@router.post("/clustering/category", tags=["database"])
async def post_clustering_category(data: List[dict] = [], db: Session = Depends(get_db)):
    stmt = insert(ClusteringCategory).values(data)
    stmt = stmt.on_duplicate_key_update(
        clustering_data=stmt.inserted.clustering_data,
    )
    db.execute(stmt)
    db.commit()
    return "OK"


# @router.get("/clustering/days", tags=["page 4"])
# async def get_clustering_days(db: Session = Depends(get_db)):
#     return db.query(ClusteringDays).limit(5).all()

# @router.post("/clustering/days", tags=["database"])
# async def post_clustering_days(data: List[dict] = [], db: Session = Depends(get_db)):
#     stmt = insert(ClusteringDays).values(data)
#     stmt = stmt.on_duplicate_key_update(
#         clustering_data=stmt.inserted.clustering_data,
#     )
#     db.execute(stmt)
#     db.commit()
#     return "OK"