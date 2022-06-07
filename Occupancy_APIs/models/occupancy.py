from datetime import datetime
from pydantic import BaseModel


class Occupancy(BaseModel):
    sensor: str
    ts: datetime = datetime.now()
    entries: int  # We can't name a field in since it's a python keyword
    out: int


"""
A sensor can have a list of occupancy
"""


class Sensor(BaseModel):
    name: str
    #occupancy: list[Occupancy] = None