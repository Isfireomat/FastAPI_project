from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.routers import routers, auth_routers, photo_routers

app:FastAPI=FastAPI(title='Tested_FastAPI_Project')
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(routers.router)
app.include_router(auth_routers.router)
app.include_router(photo_routers.router)
