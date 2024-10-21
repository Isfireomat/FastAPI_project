from fastapi import FastAPI

app:FastAPI=FastAPI(title='Tested_FastAPI_Project')

@app.get("/")
async def read_root():
    return {"Hello": "World"}

