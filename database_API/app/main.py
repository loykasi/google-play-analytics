from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .routes.transform import group_data, app_data, category_data
from .routes.websocket_connection import websocket_connection
from .routes.db_data import developers, versions, app_category, apps, categories, clustering, prediction

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_methods=["DELETE", "POST", "GET", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"]
)

app.include_router(group_data.router)
app.include_router(app_data.router)
app.include_router(category_data.router)

app.include_router(websocket_connection.router)

app.include_router(developers.router)
app.include_router(versions.router)
app.include_router(app_category.router)
app.include_router(apps.router)
app.include_router(categories.router)
app.include_router(clustering.router)
app.include_router(prediction.router)