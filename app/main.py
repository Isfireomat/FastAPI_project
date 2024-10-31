from fastapi import FastAPI, Response
from fastapi.staticfiles import StaticFiles
from app.api.routers import routers, auth_routers, photo_routers
from app.api.db_utils.db_connect import create_start_table
import asyncio

app:FastAPI=FastAPI(title='Tested_FastAPI_Project')
app.mount("/static", StaticFiles(directory="app/static"), name="static")

asyncio.run(create_start_table())

app.include_router(routers.router)
app.include_router(auth_routers.router)
app.include_router(photo_routers.router)

