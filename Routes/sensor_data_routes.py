from fastapi import APIRouter
import asyncio
from Controllers.sensor_data_controllers import combine_longitude_latitude  # Replace with actual import

router = APIRouter()
# @router.on_event("startup")
# async def startup_event():
#     asyncio.create_task(combine_longitude_latitude())