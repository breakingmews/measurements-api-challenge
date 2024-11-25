from datetime import datetime
from typing import Annotated, Sequence, Union

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from .dependencies.service import (
    MeasurementServiceDep,
)
from .dto import Info, Message
from .model import MeasurementPublic

router = APIRouter()
measurements = APIRouter()


@router.get("/info")
async def info(
    service: MeasurementServiceDep,
) -> Info:
    dataset_size = await service.get_measurements_count()
    return Info(status="running", dataset_size=dataset_size)


@measurements.get(
    "/measurements",
    response_model=Sequence[MeasurementPublic],
    responses={404: {"model": Message}},
)
async def get_measurements(
    service: MeasurementServiceDep,
    user_id: Annotated[str, Query(...)],
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 10,
    device_timestamp_from: Union[datetime, None] = Query(
        None, example="2021-02-13T00:06:00"
    ),
    device_timestamp_to: Union[datetime, None] = Query(
        None, example="2021-02-14T00:06:00"
    ),
):
    measurements = await service.get_measurements(
        user_id, offset, limit, device_timestamp_from, device_timestamp_to
    )
    if measurements:
        return measurements
    return JSONResponse(status_code=404, content={"message": "Not found"})


@measurements.get(
    "/measurements/{id}",
    response_model=MeasurementPublic,
    responses={404: {"model": Message}},
)
async def get_measurement(
    service: MeasurementServiceDep,
    id: str,
):
    measurement = await service.get_measurement(id)
    if measurement:
        return measurement
    return JSONResponse(status_code=404, content={"message": "Not found"})
