from fastapi import FastAPI, Response
from fastapi.staticfiles import StaticFiles
from app.api.routers import routers, auth_routers, photo_routers
from app.api.db_utils.db_connect import create_start_table
import asyncio
import click
from app.api.db_utils.db_connect import get_session
from fastapi import Depends, HTTPException, status, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.db_utils import db_crud
from app.api.models.schemas import UserWithPassword

app:FastAPI=FastAPI(title='Tested_FastAPI_Project')
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(routers.router)
app.include_router(auth_routers.router)
app.include_router(photo_routers.router)


if __name__=="__main__":
    asyncio.run(create_start_table())
    async def run_create_admin():
        async with get_session() as session: 
            await db_crud.create_user(session=session, 
                                    user=UserWithPassword(email="root@gmail.com", name="root", password="root"))
    import asyncio
    try:
        asyncio.run(run_create_admin())
    except:
        pass
