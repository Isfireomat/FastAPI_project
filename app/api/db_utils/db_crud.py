from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert
from pydantic import EmailStr
from passlib.context import CryptContext
from app.api.models import models, schemas
from typing import Optional, Any

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_password_hash(password: str) -> str:
    """
    Возвращаем хэш пароля
    """ 
    return pwd_context.hash(password)

async def create_user(session: AsyncSession, user: schemas.UserWithPassword) -> None:  
    """
    Вносим в БД пользователя
    """ 
    stmt = insert(models.User).values(
        email=user.email,
        name=user.name,  
        hashed_password=await get_password_hash(user.password)
    )
    await session.execute(stmt)
    await session.commit()

async def create_picture(session: AsyncSession, picture: schemas.Picture) -> None:  
    """
    Вноси в БД картинку
    """ 
    stmt = insert(models.Picture).values(binary_picture=picture.binary_picture)
    await session.execute(stmt) 
    await session.commit()

async def get_user(session: AsyncSession, user_email: EmailStr) -> Optional[models.User]: 
    """
    Получаем пользователя по email, если нету - получаем None

    result - пользователь (результат выполнения запроса)
    Возвращаем result
    """ 
    result = await session.execute(select(models.User).where(models.User.email == user_email)) 
    return result.scalar_one_or_none() 

async def get_picture_by_bytes(session: AsyncSession, binary_picture: bytes) -> Optional[models.Picture]: 
    """
    Получаем картинку по её байтам в БД, если нету - получаем None

    result - картинка (результат выполнения запроса)
    Возвращаем result
    """ 
    result = await session.execute(select(models.Picture).where(models.Picture.binary_picture == binary_picture)) 
    return result.scalar_one_or_none() 

async def get_pictures(session: AsyncSession) -> Optional[models.Picture]: 
    """
    Получаем все картинки в виде байт, если нету - возвращаем None

    result - картинки (результат выполнения запроса)
    pictures - картинки
    Возвращаем picture или None
    """ 
    result = await session.execute(select(models.Picture.binary_picture)) 
    pictures = result.scalars().all()
    return pictures if pictures else None
