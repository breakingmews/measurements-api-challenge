from pydantic import BaseModel


class Info(BaseModel):
    status: str
    dataset_size: int


class Message(BaseModel):
    message: str
