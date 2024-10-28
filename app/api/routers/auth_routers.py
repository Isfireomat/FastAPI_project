from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from typing import Any
from app.api import db_crud, schemas
from app.api.db_connect import get_session
from app.api import token_utils

router = APIRouter()
@router.post("/api/register/", response_model=dict[str, str])
async def register(response: Response, user: schemas.UserWithPassword,
                   session: AsyncSession = Depends(get_session)) -> dict[str, str]:
    db_user = await db_crud.get_user(session, user_email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    await db_crud.create_user(session=session, user=user)
    access_token_expires = timedelta(minutes=token_utils.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await token_utils.create_access_token(data={"sub": user.email}, 
                                                         expires_delta=access_token_expires)
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=token_utils.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    return {"message": "User registered successfully!"}

@router.post("/api/login", response_model=schemas.Token)
async def login(response: Response, form_data: schemas.EmailPasswordRequestForm,
                session: AsyncSession = Depends(get_session)) -> dict[str, Any]:
    user = await db_crud.get_user(session, user_email=form_data.email)
    if not user or not db_crud.pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=token_utils.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await token_utils.create_access_token(data={"sub": user.email}, 
                                                         expires_delta=access_token_expires)
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=token_utils.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "message": "Login successful"
    }

@router.post("/api/logout/")
async def logout(response: Response) -> dict[str, str]:
    response.delete_cookie("access_token")
    return {"message": "Logout successful"}
