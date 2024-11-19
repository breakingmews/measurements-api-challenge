from datetime import datetime

from sqlmodel import Field, SQLModel


class Measurement(SQLModel, table=True):
    id: str = Field(primary_key=True)
    device_id: str = Field()
    device_timestamp: datetime = Field()
    user_id: str = Field()
    value: float = Field()
