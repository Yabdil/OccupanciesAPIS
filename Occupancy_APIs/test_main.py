import json

from fastapi.testclient import TestClient
from main import app
from models.occupancy import Occupancy, Sensor

client = TestClient(app)


def test_create_sensor_success():
    sensor1 = {"sensor": "leia", "ts": "2022-06-05T18:00:00Z", "entries": 8, "out": 2}
    sensor2 = {"sensor": "syspo", "ts": "2022-06-05T18:00:00Z", "entries": 6, "out": 2}
    response1 = client.post("/api/webhook", data=json.dumps(sensor1))
    response2 = client.post("/api/webhook", data=json.dumps(sensor2))
    assert response1.status_code == 201
    assert response2.status_code == 201


def test_create_sensor_fail():
    s1 = {"ts": "2018-11-14T18:00:00Z", "entries": 2, "out": 2}
    response = client.post("/api/webhook", data=json.dumps(s1))
    assert response.status_code == 422


def test_get_list_sensors():
    response = client.get("/api/sensors")
    assert response.status_code == 200
    assert response.json() == {"sensors": ["leia", "syspo"]}


def test_get_room_occupancy():
    r1 = client.get("/api/sensors/leia/occupancy")
    r2 = client.get("/api/sensors/syspo/occupancy")

    assert r1.json()["inside"] == 6  # Testing that there is 8 entries - 2 out = 6 persons in  leia sensor
    assert r2.json()["inside"] == 4  # Testing that there is 6 entries - 2 out = 4 persons in  leia sensor


def test_get_room_with_wrong_sensor():
    fake_sensor = "X1"
    r1 = client.get(f"/api/sensors/{fake_sensor}/occupancy")
    returned_data = json.loads(r1.content)
    assert r1.status_code == 404
    assert returned_data == {fake_sensor: "sensor not found"}


def test_get_occupancy_at_given_moment():
    ts = "2022-06-05T18:00:00Z"
    response = client.get(f"/sensors/leia/occupancy?at_instant={ts}")
    assert response.status_code == 200
    assert response.json()["inside"] == 6


def test_get_occupancy_with_false_given_moment():
    ts = "2022-02-05T20:00:00Z"
    response = client.get(f"/sensors/leia/occupancy?at_instant={ts}")
    assert response.status_code == 200
    assert response.json()["inside"] == 0


"""
Since we have two sensors leia with 6 inside and syspo with 4, the api should return the room with the most
"""


def test_get_sensor_with_most_occupancies():
    response = client.get("/api/sensors/sensorWithMostOccupancies")
    assert response.json() == {"sensor": "leia", "inside": 6}
