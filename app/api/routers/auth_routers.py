from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from app.api import CRUD, schemas
from app.api.database import get_db
from app.api import cryptography

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/api/register/", response_model=schemas.User)
async def register(user: schemas.UserWithPassword, db: AsyncSession = Depends(get_db)):
    db_user = CRUD.get_user(db, user_email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return CRUD.create_user(db=db, user=user)

@router.post("/login", response_model=schemas.Token)
async def login(response: Response,form_data: schemas.EmailPasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = CRUD.get_user(db, user_email=form_data.email)
    if not user or not cryptography.pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=cryptography.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = cryptography.create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=cryptography.ACCESS_TOKEN_EXPIRE_MINUTES*60
    )
    return {"message": "Login successful"}


@router.post("/api/logout/")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logout successful"}
