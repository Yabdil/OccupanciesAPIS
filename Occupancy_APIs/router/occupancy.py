import json
from datetime import datetime

from fastapi import APIRouter, Request, Body
from fastapi.responses import JSONResponse

from models.occupancy import Sensor, Occupancy

routers = APIRouter()

data = {
}


@routers.post("/api/webhook", status_code=201)
async def create_sensor(occupancy: Occupancy):
    new_occupancy = occupancy.dict()
    name = new_occupancy['sensor']
    if name not in data:  # If it's new sensor
        data[name] = list()
        data[name].append(new_occupancy)
        return new_occupancy

    data[name].append(new_occupancy)
    return new_occupancy


@routers.get("/api/sensors", status_code=200)
async def get_list_sensors():
    sensors = [sensor for sensor in data.keys()]
    return {"sensors": sensors}


@routers.get("/api/sensors/{sensor}/occupancy", status_code=200)
async def get_room_occupancy(sensor: str):
    if sensor not in data.keys():
        return JSONResponse(content={sensor: "sensor not found"}, status_code=404)
    occupancies = data[sensor]
    entries = [occupancy["entries"] for occupancy in occupancies]  # listing all the entries
    out = [occupancy["out"] for occupancy in occupancies]  # listing all the out
    return {"sensor": sensor, "inside": sum(entries) - sum(out)}


@routers.get("/sensors/{sensor}/occupancy", status_code=200)
async def get_occupancy_at_given_moment(sensor: str, at_instant: datetime):
    if sensor not in data.keys():
        return JSONResponse(content={sensor: "sensor not found"}, status_code=404)
    occupancies = data[sensor]
    result = 0
    for occupancy in occupancies:
        if occupancy["ts"] <= at_instant:
            result += occupancy["entries"] - occupancy["out"]
    inside = result
    return {"inside": inside}


"""
BONUS
"""


@routers.get("/api/sensors/sensorWithMostOccupancies")
async def get_sensor_with_most_occupancies():
    """
    This function returns the room with the most occupancies
    :return: a Response with Dict
    """
    sensors = []
    for key, items in data.items():
        inside = 0
        sensor = {}
        for item in items:
            inside += item["entries"] - item["out"]
        sensor["sensor"] = key
        sensor["inside"] = inside
        sensors.append(sensor)
    sorted_sensors = sorted(sensors, key=lambda x: x["inside"], reverse=True)
    max_sensor_with_inside = sorted_sensors[0]
    return {'sensor': max_sensor_with_inside["sensor"], "inside": max_sensor_with_inside["inside"]}
