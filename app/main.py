from fastapi import FastAPI
from api import routers

app:FastAPI=FastAPI(title='Tested_FastAPI_Project')
app.include_router(routers.router)