import httpx
import asyncio
from Models.models import SensorData
from Connections.connections import session

async def fetch_longitude():
    async with httpx.AsyncClient() as client:
        response = await client.get('https://blynk.cloud/external/api/get?token=_wIJrhc9PmbhZcGZaqlh469aTc2k_ESq&dataStreamId=1')
        return float(response.text)

async def fetch_latitude():
    async with httpx.AsyncClient() as client:
        response = await client.get('https://blynk.cloud/external/api/get?token=_wIJrhc9PmbhZcGZaqlh469aTc2k_ESq&dataStreamId=2')
        return float(response.text)

async def add_sensor_data(longitude, latitude):
    db = session
    sensor_data = SensorData(lng=longitude, lat=latitude)
    db.add(sensor_data)
    db.commit()
    db.refresh(sensor_data)
    return sensor_data

async def combine_longitude_latitude():
    while True:
        try:
            longitude = await fetch_longitude()
            latitude = await fetch_latitude()
            await add_sensor_data(longitude, latitude)
        except Exception as e:
            print(f"Error: {e}") 
        await asyncio.sleep(30)
