from fastapi import FastAPI
from app.api.routers import routers,auth_routers

app:FastAPI=FastAPI(title='Tested_FastAPI_Project')

app.include_router(routers.router)
app.include_router(auth_routers.router)