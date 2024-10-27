from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
# from app.api.CRUD
# import app.api.cryptography
from app.api.database import get_db
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.api.cryptography import get_current_user
from fastapi.responses import RedirectResponse

router = APIRouter()
# router.mount("/static", StaticFiles(directory="app/static"), name="static")


templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def login_page(request: Request,user=Depends(get_current_user)):
    if isinstance(user, RedirectResponse):
        return user 
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/registration", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})