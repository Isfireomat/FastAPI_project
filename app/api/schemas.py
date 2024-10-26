from pydantic import BaseModel,EmailStr

class SQLAlchemyStandart(BaseModel):
    id:int
    class Config:
        orm_mode=True

class EmailPasswordRequestForm(BaseModel):
    email: EmailStr
    password: str

class User(SQLAlchemyStandart):
    email:EmailStr
    name:str

class UserWithPassword(User):
    password:str

class Picture(SQLAlchemyStandart):
    binary_picture:bytes

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str