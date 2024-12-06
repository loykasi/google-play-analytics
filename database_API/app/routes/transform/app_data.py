from fastapi import APIRouter, Response, Depends
import pandas as pd
import numpy as np
from app.config import settings
from sqlalchemy import func
from sqlalchemy.orm import Session
from ...database.database import get_db
from ...database.models import Developers, App_Category, Apps, Categories, Versions

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


@router.get("/app/histogram/score", tags=["page 2"])
async def get_score_histogram(db: Session = Depends(get_db)):
    query = (
        db.query(
            Versions.score,
        )
    )

    df = pd.read_sql(query.statement, db.bind)
    scores = df["score"].to_list()

    hist, bin_edges = np.histogram(scores, bins=np.arange(1, 5.25, 0.25))

    bin_edges = [round(h, 2) for h in bin_edges.tolist()]
    # histogram = dict(zip(bin_edges, hist.tolist()))

    return {
        "bins": bin_edges,
        "hist": hist.tolist()
    }

@router.get("/app/recent", tags=["page 1"])
async def get_recent_apps(db: Session = Depends(get_db)):
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

    query = (
        db.query(
            Versions.id,
            Versions.updated,
            Versions.title,
            Versions.icon,
            Versions.rating_1,
            Versions.rating_2,
            Versions.rating_3,
            Versions.rating_4,
            Versions.rating_5,
            genre_subquery.c.genre_id,
            genre_subquery.c.genre_name,
        )
        .join(genre_subquery, Versions.app_id == genre_subquery.c.app_id)
        .order_by(Versions.updated.desc())
        .limit(10)
    )

    df = pd.read_sql(query.statement, db.bind)

    df["date"] = pd.to_datetime(df["updated"], unit="s", utc=True)
    df["date"] = df['date'].dt.tz_convert('Asia/Bangkok')
    df["date"] = df['date'].dt.strftime('%Y-%m-%d %H:%M')
    df = df[df["date"] > '2024-10-28']

    df["type"] = df['genre_id'].apply(getType)

    return Response(df.to_json(orient="records"), media_type="application/json")

@router.get("/app/correlation", tags=["page 5"])
async def get_app_correlation(db: Session = Depends(get_db)):
    query = (
        db.query(
            Versions.installs,
            Versions.score,
            Versions.ratings,
            Versions.rating_1,
            Versions.rating_2,
            Versions.rating_3,
            Versions.rating_4,
            Versions.rating_5,
            Versions.reviews,
        )
        .order_by(Versions.updated.desc())
    )
    df = pd.read_sql(query.statement, db.bind)
    columns = ["Lượt cài đặt", "Điểm số", "Lượt đánh giá", "1 sao", "2 sao", "3 sao", "4 sao", "5 sao", "Lượt bình luận"]
    corr = df.corr()
    print(corr)
    corr_list = corr.to_numpy().tolist()
    return {
        "values": corr_list,
        "columns": columns
    }

@router.get("/app/correlation-2", tags=["page 2"])
async def get_rating_histogram(db: Session = Depends(get_db)):
    query = (
        db.query(
            Versions.installs,
            Versions.rating_5,
        )
        .order_by(Versions.updated.desc())
        .filter(
            Versions.installs < 500000000
        )
        .filter(
            Versions.rating_5 < 10000000
        )
        .limit(1000)
    )
    df = pd.read_sql(query.statement, db.bind)

    return {
        "rating_5": df["rating_5"].to_list(),
        "installs": df["installs"].to_list(),
    }