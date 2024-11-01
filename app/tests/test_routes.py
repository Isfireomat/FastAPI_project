import pytest
import pytest_asyncio
from httpx import AsyncClient
from PIL import Image
from io import BytesIO

name: str = "test_user"
email: str = "test_user@gmail.com"
password: str = "test_password"

@pytest_asyncio.fixture
async def user_data():
    return {
        "name": name,
        "email": email,
        "password": password
    }

@pytest_asyncio.fixture
async def user_data_login():
    return {
        "email": email,
        "password": password
    }

@pytest_asyncio.fixture
async def files():
    image = Image.new("RGB", (100, 100), color="red")
    byte_io = BytesIO()
    image.save(byte_io, format='JPEG')  
    byte_io.seek(0) 
    return {"photo": ("test_image.jpg", byte_io, "image/jpeg")}

@pytest_asyncio.fixture()
async def cookies(async_client: AsyncClient, user_data):
    response = await async_client.post("/api/registration/", json=user_data)
    cookies = {name: value for name, value in response.cookies.items()}
    return cookies

@pytest.mark.asyncio
async def test_index_without_regitstration(async_client: AsyncClient):
    response = await async_client.get("/")
    assert response.status_code == 307

@pytest.mark.asyncio
async def test_index_with_regitstration(async_client: AsyncClient, cookies: dict):
    response = await async_client.get("/", cookies=cookies)
    assert response.status_code == 200
    
@pytest.mark.asyncio
async def test_registration(async_client: AsyncClient, user_data):
    response = await async_client.post("/api/registration/", json=user_data)
    assert response.status_code == 200
    assert response.cookies.get("access_token" )
    assert response.cookies.get("refresh_token") 
    assert "Bearer" in response.cookies.get("access_token" )  
    assert "Bearer" in response.cookies.get("refresh_token")


@pytest.mark.asyncio
async def test_login(async_client: AsyncClient, cookies: dict, user_data_login: dict):
    response = await async_client.post("/api/login", json=user_data_login)
    assert response.status_code == 200
    assert response.cookies.get("access_token" )
    assert response.cookies.get("refresh_token") 
    assert "Bearer" in response.cookies.get("access_token" )  
    assert "Bearer" in response.cookies.get("refresh_token")


@pytest.mark.asyncio 
async def test_first_upload_picture(async_client: AsyncClient, files: dict):
    response = await async_client.post("/api/upload", files=files)
    response_data = response.json()
    assert response.status_code == 200
    assert float(response_data["result"]) == float("0")

@pytest.mark.asyncio 
async def test_second_upload_picture(async_client: AsyncClient, files: dict):
    response = await async_client.post("/api/upload", files=files)
    response_data = response.json()
    assert response.status_code == 200
    assert float(response_data["result"]) == float("0")
    response = await async_client.post("/api/upload", files=files)
    response_data = response.json()
    assert response.status_code == 200
    assert float(response_data["result"]) == float("100")
    assert response_data["picture"]

@pytest.mark.asyncio
async def test_logout(async_client: AsyncClient, cookies: dict):
    response = await async_client.post("/api/logout", cookies=cookies)
    assert response.status_code == 307
    assert response.cookies.get("access_token") is None
    assert response.cookies.get("refresh_token") is None 
    
