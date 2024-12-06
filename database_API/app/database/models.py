from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger, DECIMAL, UniqueConstraint, Date, DateTime, JSON
from sqlalchemy.orm import relationship

class Developers(Base):
    __tablename__ = "developers"

    id = Column(String, primary_key=True, index=True)
    developer = Column(String, nullable=False)


class App_Category(Base):
    __tablename__ = "app_category"

    id = Column(Integer, primary_key=True, nullable=False, index=True, autoincrement=True)
    app_id = Column(String, nullable=False)
    category_id = Column(String, nullable= False)

    __table_args__ = (UniqueConstraint("app_id", "category_id", name = "unique_app_id_category_id"),)

class Apps(Base):
    __tablename__ = "apps"

    id = Column(String, primary_key=True, nullable=False, index=True)
    developer_id = Column(String, ForeignKey("developers.id"), nullable=False)
    released = Column(String, nullable=True)

class Categories(Base):
    __tablename__ = "categories"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)

class Versions(Base):
    __tablename__ = "versions"

    id = Column(Integer, primary_key=True, nullable=False, index=True, autoincrement=True)
    app_id = Column(String, ForeignKey("apps.id"), nullable=False)
    updated = Column(BigInteger, nullable=False)
    title = Column(Integer, nullable=False)
    version = Column(String, nullable=False)
    icon = Column(String, nullable=False)
    installs = Column(BigInteger)
    score = Column(DECIMAL(8, 7), nullable=False)
    ratings = Column(BigInteger, nullable=False)
    reviews = Column(BigInteger, nullable=False)
    price = Column(Integer, nullable=False)
    currency = Column(String, nullable=False)
    rating_1 = Column(BigInteger, nullable=False)
    rating_2 = Column(BigInteger, nullable=False)
    rating_3 = Column(BigInteger, nullable=False)
    rating_4 = Column(BigInteger, nullable=False)
    rating_5 = Column(BigInteger, nullable=False)

    __table_args__ = (UniqueConstraint("app_id", "updated", name="unique_app_id_updated"),)

class ClusteringWeeks(Base):
    __tablename__ = "clustering_weeks"

    id = Column(Integer, primary_key=True, nullable=False, index=True, autoincrement=True)
    updated_date = Column(Date, nullable=False)
    clustering_data = Column(JSON, nullable=False)

class ClusteringDays(Base):
    __tablename__ = "clustering_days"

    id = Column(Integer, primary_key=True, nullable=False, index=True, autoincrement=True)
    updated_date = Column(Date, nullable=False)
    clustering_data = Column(JSON, nullable=False)

class ClusteringCategory(Base):
    __tablename__ = "clustering_category"

    id = Column(Integer, primary_key=True, nullable=False, index=True, autoincrement=True)
    updated_date = Column(Date, nullable=False)
    clustering_data = Column(JSON, nullable=False)

class ForecastDay(Base):
    __tablename__ = "forecast_days"

    id = Column(Integer, primary_key=True, nullable=False, index=True, autoincrement=True)
    predict_day = Column(Date, nullable=False)
    predict_value = Column(Integer, nullable=False)
    lower_range = Column(Integer, nullable=False)
    upper_range = Column(Integer, nullable=False)

class ForecastHour(Base):
    __tablename__ = "forecast_hours"

    id = Column(Integer, primary_key=True, nullable=False, index=True, autoincrement=True)
    predict_hour = Column(DateTime, nullable=False)
    predict_value = Column(Integer, nullable=False)
    lower_range = Column(Integer, nullable=False)
    upper_range = Column(Integer, nullable=False)