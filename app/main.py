from fastapi import FastAPI
from app.api.routers import routers,auth_routers
from fastapi.staticfiles import StaticFiles

app:FastAPI=FastAPI(title='Tested_FastAPI_Project')
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(routers.router)
app.include_router(auth_routers.router)