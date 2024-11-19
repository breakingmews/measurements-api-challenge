from datetime import datetime
from typing import Annotated, Sequence, Union

from fastapi import APIRouter, Depends, Query

from .dependencies.database import SessionDep, get_measurements, get_measurements_count
from .dto import Info
from .model import Measurement

router = APIRouter()


@router.get("/info")
async def info(dataset_size: int = Depends(get_measurements_count)) -> Info:
    return Info(status="running", dataset_size=dataset_size)


@router.get("/api/v1/levels/{user_id}")
async def levels(
    session: SessionDep,
    user_id: str,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 10,
    start: Union[datetime, None] = Query(None, example="2021-02-13T00:06:00"),
    stop: Union[datetime, None] = Query(None, example="2021-02-14T00:06:00"),
) -> Sequence[Measurement]:
    return get_measurements(session, user_id, offset, limit, start, stop)
