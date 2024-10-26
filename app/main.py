from fastapi import FastAPI
from app.api.routers import routers,auth_routers
from fastapi.staticfiles import StaticFiles
# from fastapi.middleware.cors import CORSMiddleware

app:FastAPI=FastAPI(title='Tested_FastAPI_Project')
# from fastapi.middleware.cors import CORSMiddleware

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(routers.router)
app.include_router(auth_routers.router)