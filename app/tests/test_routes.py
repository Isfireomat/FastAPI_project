import pytest
from httpx import AsyncClient
from PIL import Image
from app.api.utils.picture_utils import image_to_bytes

@pytest.fixture
def picture_data():
    original_image = Image.new("RGB", (100, 100), color="red")
    file_name = "test_image.png"
    return {"photo": (file_name, image_to_bytes(original_image), "image/png")}

@pytest.mark.asyncio
async def test_index_withou_login(async_client: AsyncClient):
    response = await async_client.post("/")
    assert response.status_code == 302

@pytest.mark.asyncio
async def test_registration(async_client: AsyncClient):
    user_data = {"username": "test_user",
                 "email":"test666@gmail.com",
                 "password":"test_password"}
    response = await async_client.post("/api/registration", json=user_data)
    response_data = response.json()
    assert response.status_code == 201
    assert "access_token" in response_data 
    assert "refresh_token" in response_data 
    assert "Bearer" in response_data["access_token"]  
    assert "Bearer" in response_data["refresh_token"]

@pytest.mark.asyncio
async def test_login(async_client: AsyncClient):
    user_data = {"email":"test666@gmail.com",
                 "password":"test_password"}
    response = await async_client.post("/api/login", json=user_data)
    response_data = response.json()
    assert response.status_code == 201
    assert "access_token" in response_data 
    assert "refresh_token" in response_data 
    assert "Bearer" in response_data["access_token"]  
    assert "Bearer" in response_data["refresh_token"] 

@pytest.mark.asyncio 
async def test_first_upload_picture(async_client: AsyncClient, picture_data: dict):
    response = await async_client.post("/api/upload", file=picture_data)
    response_data = response.json()
    assert response.status_code == 201
    assert response_data["result"] == "0"

@pytest.mark.asyncio 
async def test_second_upload_picture(async_client: AsyncClient, picture_data: dict):
    response = await async_client.post("/api/upload", file=picture_data)
    response_data = response.json()
    assert response.status_code == 200
    assert response_data["result"] == "100"

@pytest.mark.asyncio
async def test_logout(async_client: AsyncClient):
    response = await async_client.post("/api/logout")
    response_data = response.json()
    assert response.status_code == 200
    assert "access_token" not in response_data 
    assert "refresh_token" not in response_data 
    
