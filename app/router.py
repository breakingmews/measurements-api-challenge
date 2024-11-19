from datetime import datetime
from typing import Annotated, Sequence, Union

from fastapi import APIRouter, Depends, Query

from .dependencies.database import SessionDep, get_measurements, get_measurements_count
from .dto import Info
from .model import MeasurementPublic

router = APIRouter()
measurements = APIRouter()


@router.get("/info")
async def info(dataset_size: int = Depends(get_measurements_count)) -> Info:
    return Info(status="running", dataset_size=dataset_size)


@measurements.get("/levels")
async def levels(
    session: SessionDep,
    user_id: Annotated[str, Query(...)],
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 10,
    device_timestamp_from: Union[datetime, None] = Query(
        None, example="2021-02-13T00:06:00"
    ),
    device_timestamp_to: Union[datetime, None] = Query(
        None, example="2021-02-14T00:06:00"
    ),
) -> Sequence[MeasurementPublic]:
    return get_measurements(
        session, user_id, offset, limit, device_timestamp_from, device_timestamp_to
    )
