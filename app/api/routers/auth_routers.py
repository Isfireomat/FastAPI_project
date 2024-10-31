from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from typing import Any
from app.api.db_utils import db_crud
from app.api.models import schemas
from app.api.db_utils.db_connect import get_session
from app.api.utils import token_utils

router = APIRouter()
@router.post("/api/register/", response_model=dict[str, str])
async def register(response: Response, user: schemas.UserWithPassword,
                   session: AsyncSession = Depends(get_session)) -> dict[str, str]:
    """
    Эндпоин регистрации
    """
    db_user = await db_crud.get_user(session, user_email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    await db_crud.create_user(session=session, user=user)
    refresh_token = await token_utils.create_refresh_token(data={"sub": user.email}, 
                                                         expires_delta=token_utils.REFRESH_TOKEN_EXPIRE_MINUTES)
    access_token = await token_utils.create_access_token(data={"sub": user.email}, 
                                                         expires_delta=token_utils.ACCESS_TOKEN_EXPIRE_MINUTES)
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=int(token_utils.ACCESS_TOKEN_EXPIRE_MINUTES.total_seconds())
    )
    response.set_cookie(
        key="refresh_token",
        value=f"Bearer {refresh_token}",
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=int(token_utils.REFRESH_TOKEN_EXPIRE_MINUTES.total_seconds())
    )
    return {"message": "User registered successfully!"}

@router.post("/api/login", response_model=schemas.Token)
async def login(response: Response, form_data: schemas.EmailPasswordRequestForm,
                session: AsyncSession = Depends(get_session)) -> dict[str, Any]:
    """
    Эндпоин авторизации
    """
    user = await db_crud.get_user(session, user_email=form_data.email)
    if not user or not db_crud.pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    refresh_token = await token_utils.create_refresh_token(data={"sub": user.email}, 
                                                         expires_delta=token_utils.REFRESH_TOKEN_EXPIRE_MINUTES)
    access_token = await token_utils.create_access_token(data={"sub": user.email}, 
                                                         expires_delta=token_utils.ACCESS_TOKEN_EXPIRE_MINUTES)
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=int(token_utils.ACCESS_TOKEN_EXPIRE_MINUTES.total_seconds())
    )
    response.set_cookie(
        key="refresh_token",
        value=f"Bearer {refresh_token}",
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=int(token_utils.REFRESH_TOKEN_EXPIRE_MINUTES.total_seconds())
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "message": "Login successful"
    }

@router.post("/api/logout/")
async def logout(response: Response) -> dict[str, str]:
    """
    Эндпоинт выхода
    """
    response.delete_cookie("access_token")
    return {"message": "Logout successful"}
