from datetime import datetime
from typing import Annotated, Optional, Sequence, Union

from fastapi import APIRouter, Depends, Query

from .dependencies.service import MeasurementService, get_measurement_service
from .dto import Info
from .model import MeasurementPublic

router = APIRouter()
measurements = APIRouter()


@router.get("/info")
async def info(
    service: MeasurementService = Depends(get_measurement_service),
) -> Info:
    dataset_size = await service.get_measurements_count()
    return Info(status="running", dataset_size=dataset_size)


@measurements.get("/levels")
async def levels(
    user_id: Annotated[str, Query(...)],
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 10,
    device_timestamp_from: Union[datetime, None] = Query(
        None, example="2021-02-13T00:06:00"
    ),
    device_timestamp_to: Union[datetime, None] = Query(
        None, example="2021-02-14T00:06:00"
    ),
    service: MeasurementService = Depends(get_measurement_service),
) -> Sequence[MeasurementPublic]:
    return await service.get_measurements(
        user_id, offset, limit, device_timestamp_from, device_timestamp_to
    )


@measurements.get("/levels/{id}")
async def level(
    id: str,
    service: MeasurementService = Depends(get_measurement_service),
) -> Optional[MeasurementPublic]:
    return await service.get_measurement(id)
