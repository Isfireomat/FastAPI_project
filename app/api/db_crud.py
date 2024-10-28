from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert
from pydantic import EmailStr
from passlib.context import CryptContext
from app.api import models, schemas
from typing import Optional, Any

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_password_hash(password: str) -> str: 
    return pwd_context.hash(password)

async def create_user(session: AsyncSession, user: schemas.UserWithPassword) -> None:  
    stmt = insert(models.User).values(
        email=user.email,
        name=user.name,  
        hashed_password=await get_password_hash(user.password)
    )
    await session.execute(stmt)
    await session.commit()

async def create_picture(session: AsyncSession, picture: schemas.Picture) -> None:  
    stmt = insert(models.Picture).values(binary_picture=picture.binary_picture)
    await session.execute(stmt) 
    await session.commit()

async def get_user(session: AsyncSession, user_email: EmailStr) -> Optional[models.User]: 
    result = await session.execute(select(models.User).where(models.User.email == user_email)) 
    return result.scalar_one_or_none() 