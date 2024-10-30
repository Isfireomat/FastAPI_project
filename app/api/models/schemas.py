from pydantic import BaseModel,EmailStr

class SQLAlchemyStandart(BaseModel):
    """
    Тут то, что есть во всех таблицах БД
    """ 
    id:int
    class Config:
        from_attributes=True

class EmailPasswordRequestForm(BaseModel):
    """
    Валидация для формы авторизации
    """ 
    email: EmailStr
    password: str

class User(SQLAlchemyStandart):
    """
    Валидация данных пользователя из БД
    """ 
    email:EmailStr
    name:str

class UserWithPassword(BaseModel):
    """
    Валидация для формы регистрации
    """ 
    name: str
    email: EmailStr
    password: str

class Picture(BaseModel):
    """
    Валидация картинок
    """ 
    binary_picture:bytes

class Token(BaseModel):
    """
    Валидация токенов
    """ 
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """
    Валидация данных токена
    """ 
    username: str