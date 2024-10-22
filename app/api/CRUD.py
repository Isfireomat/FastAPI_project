from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import EmailStr
from api import models, schemas, cryptography

async def create_user(db: AsyncSession, user: schemas.UserWithPassword):
    db.add(models.user(name=user.name, email=user.email, hashed_password=cryptography.get_password_hash(user.password)))
    await db.commit()

async def create_picture(db:AsyncSession,pictur: schemas.Picture):
    db.add(models.pictur(binary_picture=pictur.binary_picture))
    await db.commit()

async def validate_user(db: AsyncSession, user_email:EmailStr, password:str):
    return await hash(password)==db.execute(select(models.user.c.hashed_password).where(models.user.c.email==user_email))

async def get_user(db: AsyncSession, user_email: EmailStr):
    return await db.execute(select(models.user).where(models.user.c.email==user_email)).first()
