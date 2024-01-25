from fastapi import APIRouter, HTTPException
import asyncio
from Controllers.admin_controller import create_admin,login
router = APIRouter()

# create admin
@router.post("/create_admin")
async def create_admin_route():
    try:
        return await create_admin()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
# login admin
@router.post("/login")
async def login_route(admin:dict):
    try:
        return await login(admin)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    