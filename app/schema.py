import datetime
from typing import Literal
from pydantic import BaseModel

class OkResponse(BaseModel):
    status: Literal['ok']

class GetAdvertisementResponse(BaseModel):
    id: int
    title: str
    description: str
    author: str
    price: float
    date_of_creation: datetime.datetime

class CreateAdvertisementRequest(BaseModel):
    title: str
    description: str
    author: str
    price: float

class CreateAdvertisementResponse(BaseModel):
    id: int

class UpdateAdvertisementRequest(BaseModel):
    title: str
    description: str
    author: str
    price: float

class UpdateAdvertisementResponse(CreateAdvertisementResponse):
    pass
