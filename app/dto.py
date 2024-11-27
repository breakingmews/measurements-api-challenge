from typing import Sequence

from pydantic import BaseModel

from app.model import MeasurementPublic


class Info(BaseModel):
    status: str
    dataset_size: int


class Message(BaseModel):
    message: str


class MeasurementsResponse(BaseModel):
    measurements: Sequence[MeasurementPublic]
