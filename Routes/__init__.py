from fastapi import APIRouter
from Controllers import sensor_data

router = APIRouter()

@router.post("/sensor-data/")
def create_sensor_data(longitude: float, latitude: float):
    return sensor_data(longitude, latitude)
