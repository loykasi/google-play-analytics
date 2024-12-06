from fastapi import APIRouter, Response, Depends, Path
import pandas as pd
import json
from typing import Annotated

from sqlalchemy import func
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


@router.get("/group/genre/app/{count}", tags=["page 3"])
async def get_genre_app(
    count: Annotated[int, Path(title="Days count")],
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
    start_date = datetime(now.year, now.month, now.day) - timedelta(days=count - 1)
    start_date = start_date.timestamp()    
    
    query = (
        db.query(
            Versions.updated,
            Versions.score,
            genre_subquery.c.genre_id,
            genre_subquery.c.genre_name,
        )
        .join(genre_subquery, Versions.app_id == genre_subquery.c.app_id)
        .order_by(Versions.updated.desc())
        .filter(
            Versions.updated > start_date if count != 0 else True
        )
    )

    df = pd.read_sql(query.statement, db.bind)

    df["date"] = pd.to_datetime(df["updated"], unit="s", utc=True)
    df["date"] = df['date'].dt.tz_convert('Asia/Bangkok')
    df["date"] = df['date'].dt.strftime('%Y-%m-%d')
    df = df[df["date"] > '2024-10-28']

    df["type"] = df['genre_id'].apply(getType)
    df = df[df["type"] == "app"]

    category = df.groupby("genre_name").agg(
        count=('genre_name', 'size'),
        avg_score=('score', 'mean'),
    ).reset_index()

    category = category.sort_values(by='count', ascending=False)
    category = category.rename(columns={"genre_name": "genre"})
    category = category.head(20)

    return Response(category.to_json(orient="records"), media_type="application/json")

@router.get("/group/genre/game/{count}", tags=["page 3"])
async def get_genre_game(
    count: Annotated[int, Path(title="Days count")],
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
    start_date = datetime(now.year, now.month, now.day) - timedelta(days=count - 1)
    start_date = start_date.timestamp()    
    
    query = (
        db.query(
            Versions.updated,
            Versions.score,
            genre_subquery.c.genre_id,
            genre_subquery.c.genre_name,
        )
        .join(genre_subquery, Versions.app_id == genre_subquery.c.app_id)
        .order_by(Versions.updated.desc())
        .filter(
            Versions.updated > start_date if count != 0 else True
        )
    )

    df = pd.read_sql(query.statement, db.bind)

    df["date"] = pd.to_datetime(df["updated"], unit="s", utc=True)
    df["date"] = df['date'].dt.tz_convert('Asia/Bangkok')
    df["date"] = df['date'].dt.strftime('%Y-%m-%d')
    df = df[df["date"] > '2024-10-28']

    df["type"] = df['genre_id'].apply(getType)
    df = df[df["type"] == "game"]

    category = df.groupby("genre_name").agg(
        count=('genre_name', 'size'),
        avg_score=('score', 'mean'),
    ).reset_index()

    category = category.sort_values(by='count', ascending=False)
    category = category.rename(columns={"genre_name": "genre"})
    category = category.head(20)

    return Response(category.to_json(orient="records"), media_type="application/json")

@router.get("/group/genre/{count}")
async def get_genre(
    count: Annotated[int, Path(title="Days count")],
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
    start_date = datetime(now.year, now.month, now.day) - timedelta(days=count - 1)
    start_date = start_date.timestamp()    
    
    query = (
        db.query(
            Versions.updated,
            Versions.score,
            genre_subquery.c.genre_id,
            genre_subquery.c.genre_name,
        )
        .join(genre_subquery, Versions.app_id == genre_subquery.c.app_id)
        .order_by(Versions.updated.desc())
        .filter(
            Versions.updated > start_date if count != 0 else True
        )
    )

    df = pd.read_sql(query.statement, db.bind)

    df["date"] = pd.to_datetime(df["updated"], unit="s", utc=True)
    df["date"] = df['date'].dt.tz_convert('Asia/Bangkok')
    df["date"] = df['date'].dt.strftime('%Y-%m-%d')
    df = df[df["date"] > '2024-10-28']

    df["type"] = df['genre_id'].apply(getType)

    category = df.groupby("genre_name").agg(
        count=('genre_name', 'size'),
        avg_score=('score', 'mean'),
    ).reset_index()

    category = category.sort_values(by='count', ascending=False)
    category = category.rename(columns={"genre_name": "genre"})

    return Response(category.to_json(orient="records"), media_type="application/json")

@router.get("/group/category/{count}")
async def get_genre(
    count: Annotated[int, Path(title="Days count")],
    db: Session = Depends(get_db)
):
    categories_subquery = (
        db.query(
            App_Category.app_id,
            func.json_arrayagg(Categories.name).label("categories")
        )
        .join(Categories, App_Category.category_id == Categories.id)
        .group_by(App_Category.app_id)
        .subquery()
    )

    now = datetime.now(timezone.utc)
    start_date = datetime(now.year, now.month, now.day) - timedelta(days=count - 1)
    start_date = start_date.timestamp()    
    
    query = (
        db.query(
            Versions.updated,
            categories_subquery.c.categories,
        )
        .join(categories_subquery, Versions.app_id == categories_subquery.c.app_id)
        .order_by(Versions.updated.desc())
        .filter(
            Versions.updated > start_date if count != 0 else True
        )
    )

    df = pd.read_sql(query.statement, db.bind)

    df["date"] = pd.to_datetime(df["updated"], unit="s", utc=True)
    df["date"] = df['date'].dt.tz_convert('Asia/Bangkok')
    df["date"] = df['date'].dt.strftime('%Y-%m-%d')
    df = df[df["date"] > '2024-10-28']

    df['categories'] = df['categories'].apply(json.loads)

    df = df[["categories"]]

    return {
        "categories": df["categories"].to_list()
    }