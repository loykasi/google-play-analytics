from fastapi import APIRouter, Response, Depends
import pandas as pd
from typing import List

from sqlalchemy.orm import Session
from sqlalchemy.dialects.mysql import insert
from ...database.database import get_db
from ...database.models import Versions, ForecastDay, ForecastHour

router = APIRouter()

@router.get("/prediction/update-count-day", tags=["page 1"])
async def get_prediction_update_day(db: Session = Depends(get_db)):
    query = (
        db.query(
            ForecastDay.predict_day,
            ForecastDay.predict_value,
        )
        .order_by(ForecastDay.predict_day.desc())
        .limit(1)
    )
    df = pd.read_sql(query.statement, db.bind)

    return Response(df.to_json(orient="records", date_format="iso"), media_type="application/json")

    
@router.get("/prediction/update-count-hour", tags=["page 1"])
async def get_prediction_update_hour(db: Session = Depends(get_db)):
    query = (
        db.query(
            ForecastHour.predict_hour,
            ForecastHour.predict_value,
        )
        .order_by(ForecastHour.predict_hour.desc())
        .limit(3)
    )
    df = pd.read_sql(query.statement, db.bind)
    df = df.iloc[::-1]
    return Response(df.to_json(orient="records", date_format="iso"), media_type="application/json")

    # query_lastest_time = (
    #     db.query(
    #         Versions.updated,
    #     )
    #     .order_by(Versions.updated.desc())
    #     .limit(1)
    # )
    # df = pd.read_sql(query_lastest_time.statement, db.bind)
    # df["updated"] = pd.to_datetime(df["updated"], unit="s").dt.strftime('%Y-%m-%d %H')
    # date_hour = df["updated"].iloc[0]
    
    # query = (
    #     db.query(
    #         ForecastHour.predict_hour,
    #         ForecastHour.predict_value,
    #     )
    #     .filter(
    #         ForecastHour.predict_hour >= date_hour
    #     )
    #     .order_by(ForecastHour.predict_hour.asc())
    #     .limit(3)
    # )

@router.post("/prediction/day", tags=["database"])
async def post_prediction_day(data: List[dict] = [], db: Session = Depends(get_db)):
    stmt = insert(ForecastDay).values(data)
    stmt = stmt.on_duplicate_key_update(
        predict_value=stmt.inserted.predict_value,
        lower_range=stmt.inserted.lower_range,
        upper_range=stmt.inserted.upper_range
    )
    db.execute(stmt)
    db.commit()
    return "OK"

@router.post("/prediction/hour", tags=["database"])
async def post_prediction_hour(data: List[dict] = [], db: Session = Depends(get_db)):
    stmt = insert(ForecastHour).values(data)
    stmt = stmt.on_duplicate_key_update(
        predict_value=stmt.inserted.predict_value,
        lower_range=stmt.inserted.lower_range,
        upper_range=stmt.inserted.upper_range
    )
    db.execute(stmt)
    db.commit()
    return "OK"