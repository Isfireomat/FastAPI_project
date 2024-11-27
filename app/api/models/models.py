from sqlalchemy import Column, Integer, String, \
                       LargeBinary, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    """
    Модель пользователя
    """ 
    __tablename__ = 'users'
    
    id: int = Column(Integer, primary_key=True) 
    email: str = Column(String, nullable=False, unique=True)  
    is_super: bool = Column(Boolean, nullable=False, default=False)
    name: str = Column(String, nullable=False)
    hashed_password: str = Column(String, nullable=False)
    pictures = relationship("Picture", back_populates="user")

class Picture(Base):
    """
    Модель картинок
    """ 
    __tablename__ = 'pictures'
    
    id: int = Column(Integer, primary_key=True) 
    binary_picture: bytes = Column(LargeBinary, nullable=False, unique=True)
    title: str = Column(String, nullable=False)
    user_id: int = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="pictures",  lazy='joined')
    is_active: bool = Column(Boolean, default=False)