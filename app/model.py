from sqlmodel import Field, SQLModel


class Measurement(SQLModel, table=True):
    serial_number: str = Field(primary_key=True)
    device_timestamp: str = Field(primary_key=True)
    user_id: str = Field()
    glucose_value_mgdl: float = Field(default=None)
