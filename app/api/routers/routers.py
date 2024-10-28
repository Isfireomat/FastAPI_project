from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from app.api.token_utils import get_current_user

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def login_page(request: Request, 
                     user: dict | RedirectResponse = Depends(get_current_user)) -> HTMLResponse:
    if isinstance(user, RedirectResponse):
        return user 
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/registration", response_class=HTMLResponse)
async def registration_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("registration.html", {"request": request})

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("login.html", {"request": request})
