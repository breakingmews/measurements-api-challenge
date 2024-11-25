from datetime import datetime
from typing import Annotated, Optional, Sequence, Union

from fastapi import Depends
from sqlmodel import Session, col, func, select

from app.model import Measurement

from .database import SessionDep


class MeasurementService:
    def __init__(self, session: SessionDep):
        self.session: Session = session

    async def get_measurements_count(self):
        return self.session.scalar(select(func.count()).select_from(Measurement)) or 0

    async def get_measurements(
        self,
        user_id: str,
        offset: int,
        limit: int,
        device_timestamp_from: Union[datetime, None] = None,
        device_timestamp_to: Union[datetime, None] = None,
    ) -> Sequence[Measurement]:
        query = (
            select(Measurement)
            .where(Measurement.user_id == user_id)
            .offset(offset)
            .limit(limit)
        )
        if device_timestamp_from:
            query = query.where(Measurement.device_timestamp >= device_timestamp_from)
        if device_timestamp_to:
            query = query.where(Measurement.device_timestamp <= device_timestamp_to)
        query = query.order_by(col(Measurement.device_timestamp).desc())

        return self.session.exec(query).all()

    async def get_measurement(self, id: str) -> Optional[Measurement]:
        query = select(Measurement).where(Measurement.id == id)
        return self.session.exec(query).one_or_none()


def get_measurement_service(session: SessionDep) -> MeasurementService:
    return MeasurementService(session)


MeasurementServiceDep = Annotated[MeasurementService, Depends(get_measurement_service)]
