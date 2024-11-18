import logging
from typing import Annotated, Sequence

import pandas as pd
from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine, func, select

from app.config import settings
from app.dependencies.dataset import load_dataset
from app.model import Measurement

_log = logging.getLogger(__name__)

engine = create_engine(**settings.db)  # type: ignore


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    _log.info("Created database and tables")


def import_dataset():
    session = next(get_session())
    count = get_measurements_count(session)
    if count > 0:
        _log.info(f"Dataset already imported: {count} records")
        return

    dataset: pd.DataFrame = load_dataset()
    records = dataset.to_dict(orient="records")

    for i, record in enumerate(records):
        _log.debug(f"Record {i + 1}/{len(records)}: {record}")
        session.add(Measurement(**record))
        session.commit()


def get_measurements_count(session: SessionDep):
    return session.scalar(select(func.count()).select_from(Measurement)) or 0


def get_measurements(
    user_id: str, offset: int, limit: int, session: SessionDep
) -> Sequence[Measurement]:
    return session.exec(
        select(Measurement)
        .where(Measurement.user_id == user_id)
        .offset(offset)
        .limit(limit)
    ).all()
