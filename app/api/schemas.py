from pydantic import BaseModel,EmailStr

class SQLAlchemyStandart(BaseModel):
    id:int
    class Config:
        orm_mode=True

class User(SQLAlchemyStandart):
    email:EmailStr
    username:str

class UserWithPassword(User):
    password:str
   

class Picture(SQLAlchemyStandart):
    binary_picture:bin

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str