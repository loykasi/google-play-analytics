from fastapi import APIRouter, Path, Response, Depends
import pandas as pd
from collections import Counter
from typing import Annotated
from sqlalchemy import func, and_
from sqlalchemy.orm import Session
from ...database.database import get_db
from ...database.models import Developers, App_Category, Apps, Categories, Versions

from datetime import datetime, timedelta, timezone

router = APIRouter()

game_genres = [
    "NGUOI_NOI_TIENG_VA_THAN_TUONG",
    "LANG_MAN",
    "QUAI_VAT",
    "NAU_AN",
    "THAY_MA",
    "TAO_KIEU",
    "NHIEU_NGUOI_CHOI",
    "NEN_VAN_MINH"
    ]

def getType(value):
    if "GAME" in value:
        return "game"
    elif value in game_genres:
        return "game"
    return "app"


@router.get("/group/hour/{count}", tags=["page 1"])
async def get_recent_hour_updated(
    count: Annotated[int, Path(title="Hours count")],
    skip_current: bool = False,
    db: Session = Depends(get_db)
):
    query_lastest_time = (
        db.query(
            Versions.updated,
        )
        .order_by(Versions.updated.desc())
        .limit(1)
    )
    df = pd.read_sql(query_lastest_time.statement, db.bind)
    df["updated"] = pd.to_datetime(df["updated"], unit="s")
    date_hour = df["updated"].iloc[0]


    row_genre_subquery = (
        db.query(
            App_Category,
            func.row_number().over(partition_by=App_Category.app_id, order_by=App_Category.id).label('rn')
        )
        .subquery()
    )

    genre_subquery = (
        db.query(
            row_genre_subquery.c.app_id,
            row_genre_subquery.c.category_id.label('genre_id'),
            Categories.name.label('genre_name')
        )
        .join(Categories, row_genre_subquery.c.category_id == Categories.id)
        .filter(row_genre_subquery.c.rn == 1)
        .subquery()
    )

    now = date_hour
    current_date = now.replace(minute=0, second=0, microsecond=0)
    start_date = current_date - timedelta(hours=count if skip_current else count - 1)
    current_date = current_date.timestamp()
    start_date = start_date.timestamp()
    
    query = (
        db.query(
            Versions.updated,
            genre_subquery.c.genre_id,
            genre_subquery.c.genre_name,
        )
        .join(genre_subquery, Versions.app_id == genre_subquery.c.app_id)
        .order_by(Versions.updated.desc())
        .filter(
            Versions.updated < current_date if skip_current else True
        )
        .filter(
            Versions.updated > start_date if count != 0 else True
        )
    )

    df = pd.read_sql(query.statement, db.bind)

    if df.shape[0] > 0:
        df["date_hour"] = pd.to_datetime(df["updated"], unit="s", utc=True)
        df["date_hour"] = df['date_hour'].dt.tz_convert('Asia/Bangkok')
        df["date_hour"] = df['date_hour'].dt.strftime('%Y-%m-%d %H')
        df = df[df["date_hour"] > '2024-10-28']

        df["type"] = df['genre_id'].apply(getType)
        df = df.groupby('date_hour').agg({
            'updated': 'count',
            'type': lambda x: dict(Counter(x)),
        }).reset_index()

        df = df.rename(columns={'installs': 'totalInstalls', 'reviews': 'totalReviews'})
        df = df.join(pd.json_normalize(df['type'])).drop('type', axis='columns')
        if 'app' not in df.columns:
            df['app'] = 0
        if 'game' not in df.columns:
            df['game'] = 0
        df['app'] = df['app'].fillna(0)
        df['game'] = df['game'].fillna(0)
        df = df.astype({
            'app': int,
            'game': int
        })

    return Response(df.to_json(orient="records"), media_type="application/json")

@router.get("/group/day/{count}", tags=["page 2"])
async def get_recent_day_updated(
    count: Annotated[int, Path(title="Days count")],
    skip_current: bool = False,
    db: Session = Depends(get_db)
):
    row_genre_subquery = (
        db.query(
            App_Category,
            func.row_number().over(partition_by=App_Category.app_id, order_by=App_Category.id).label('rn')
        )
        .subquery()
    )

    genre_subquery = (
        db.query(
            row_genre_subquery.c.app_id,
            row_genre_subquery.c.category_id.label('genre_id'),
            Categories.name.label('genre_name')
        )
        .join(Categories, row_genre_subquery.c.category_id == Categories.id)
        .filter(row_genre_subquery.c.rn == 1)
        .subquery()
    )

    now = datetime.now(timezone.utc)
    current_date = datetime(now.year, now.month, now.day)
    start_date = current_date - timedelta(days=count if skip_current else count - 1)
    current_date = current_date.timestamp()
    start_date = start_date.timestamp()
    query = (
        db.query(
            Versions.updated,
            genre_subquery.c.genre_id,
            genre_subquery.c.genre_name,
        )
        .join(genre_subquery, Versions.app_id == genre_subquery.c.app_id)
        .order_by(Versions.updated.desc())
        .filter(
            Versions.updated < current_date if skip_current else True
        )
        .filter(
            Versions.updated > start_date if count != 0 else True
        )
    )

    df = pd.read_sql(query.statement, db.bind)
    
    if df.shape[0] > 0:
        df["date"] = pd.to_datetime(df["updated"], unit="s", utc=True)
        df["date"] = df['date'].dt.tz_convert('Asia/Bangkok')
        df["date"] = df['date'].dt.strftime('%Y-%m-%d')
        df = df[df["date"] > '2024-10-28']

        df["type"] = df['genre_id'].apply(getType)
        df = df.groupby('date').agg({
            'updated': 'count',
            'type': lambda x: dict(Counter(x)),
        }).reset_index()

        df = df.rename(columns={'installs': 'totalInstalls', 'reviews': 'totalReviews'})
        df = df.join(pd.json_normalize(df['type'])).drop('type', axis='columns')
        if 'app' not in df.columns:
            df['app'] = 0
        if 'game' not in df.columns:
            df['game'] = 0
        df['app'] = df['app'].fillna(0)
        df['game'] = df['game'].fillna(0)
        df = df.astype({
            'app': int,
            'game': int
        })

    return Response(df.to_json(orient="records"), media_type="application/json")