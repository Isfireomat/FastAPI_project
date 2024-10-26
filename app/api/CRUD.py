from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert
from pydantic import EmailStr
from app.api import models, schemas
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
 
async def get_password_hash(password):
    return pwd_context.hash(password)

async def create_user(db: AsyncSession, user: schemas.UserWithPassword):
    stmt = insert(models.user).values(
        email=user.email,
        username=user.name,
        hashed_password=await get_password_hash(user.password)
    )
    await db.execute(stmt)
    await db.commit()

async def create_picture(db:AsyncSession,pictur: schemas.Picture):
    db.add(models.pictur(binary_picture=pictur.binary_picture))
    await db.commit()

async def get_user(db: AsyncSession, user_email: EmailStr):
    result=await db.execute(select(models.user).where(models.user.c.email==user_email))
    return result.first()
    