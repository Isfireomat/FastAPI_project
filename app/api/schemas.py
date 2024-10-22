from pydantic import BaseModel,EmailStr

class SQLAlchemyStandart(BaseModel):
    id:int
    class Config:
        orm_mode=True

class User(SQLAlchemyStandart):
    email:EmailStr
    username:str
    hashed_password:str
   

class Picture(SQLAlchemyStandart):
    binary_picture:bin
