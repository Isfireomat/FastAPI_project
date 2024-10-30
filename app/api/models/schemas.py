from pydantic import BaseModel,EmailStr

class SQLAlchemyStandart(BaseModel):
    id:int
    class Config:
        from_attributes=True

class EmailPasswordRequestForm(BaseModel):
    email: EmailStr
    password: str

class User(SQLAlchemyStandart):
    email:EmailStr
    name:str

class UserWithPassword(BaseModel):
    name: str
    email: EmailStr
    password: str

class Picture(BaseModel):
    binary_picture:bytes

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str