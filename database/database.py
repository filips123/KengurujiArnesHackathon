from __future__ import annotations

from datetime import datetime, timedelta
from typing import Annotated

from sqlalchemy import (
    ForeignKey,
    Index,
    Text,
    create_engine,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    relationship,
)

intpk = Annotated[int, mapped_column(primary_key=True)]
text = Annotated[str, mapped_column(Text())]


class Base(DeclarativeBase):
    pass


class HydroStation(Base):
    __tablename__ = "hydro_stations"

    id: Mapped[intpk]

    key: Mapped[int] = mapped_column(index=True)
    name: Mapped[text]
    river: Mapped[text]

    latitude: Mapped[float]
    longitude: Mapped[float]
    altitude: Mapped[float]


class MeteoStation(Base):
    __tablename__ = "meteo_stations"

    id: Mapped[intpk]

    key: Mapped[int] = mapped_column(index=True)
    name: Mapped[text]

    latitude: Mapped[float]
    longitude: Mapped[float]
    altitude: Mapped[float]


class HydroMeasurement(Base):
    __tablename__ = "hydro_measurements"
    __table_args__ = (Index("ix_hydro_measurements_station_datetime", "station_id", "datetime"),)

    id: Mapped[intpk]

    station_id: Mapped[int] = mapped_column(ForeignKey("hydro_stations.key"), index=True)
    station: Mapped[HydroStation] = relationship()

    datetime: Mapped[datetime]
    level: Mapped[float | None]
    flow: Mapped[float | None]
    temperature: Mapped[float | None]


class MeteoMeasurement(Base):
    __tablename__ = "meteo_measurements"
    __table_args__ = (Index("ix_meteo_measurements_station_datetime", "station_id", "datetime"),)

    id: Mapped[intpk]

    station_id: Mapped[int] = mapped_column(ForeignKey("meteo_stations.key"), index=True)
    station: Mapped[MeteoStation] = relationship()

    datetime: Mapped[datetime] = mapped_column(index=True)
    temperature: Mapped[float | None]
    precipitation: Mapped[float | None]


class Prediction(Base):
    __tablename__ = "predictions"
    __table_args__ = (Index("ix_predictions_station_datetime_future", "station_id", "datetime", "future"),)

    id: Mapped[intpk]

    station_id: Mapped[int] = mapped_column(ForeignKey("meteo_stations.key"), index=True)
    station: Mapped[MeteoStation] = relationship()

    datetime: Mapped[datetime]  # Latest data from which prediction was generated
    future: Mapped[timedelta]  # For how far in the future prediction was generated

    prediction: Mapped[float]


engine = create_engine("sqlite:///measurements.db")
session = Session(engine)

Base.metadata.create_all(engine)
