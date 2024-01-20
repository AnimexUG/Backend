from fastapi import APIRouter, HTTPException
import asyncio
from Controllers.sensor_data_controllers import get_device_data,get_unique_device_ids
router = APIRouter()
# @router.on_event("startup")
# async def startup_event():
#     asyncio.create_task(combine_longitude_latitude())

@router.get("/device/")
async def read_device_data(device_id: str):
    try:
        data = await get_device_data(device_id)
        if not data:
            raise HTTPException(status_code=404, detail="Device not found")
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# get unique device id
@router.get("/device/unique")
async def read_unique_device_id():
    devices = await get_unique_device_ids()
    return {"devices": devices}