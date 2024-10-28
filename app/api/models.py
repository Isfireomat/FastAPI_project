from sqlalchemy import Column, Integer, String, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from typing import Optional

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id: int = Column(Integer, primary_key=True) 
    email: str = Column(String, nullable=False, unique=True)  
    name: str = Column(String, nullable=False)
    hashed_password: str = Column(String, nullable=False)

class Picture(Base):
    __tablename__ = 'pictures'
    
    id: int = Column(Integer, primary_key=True) 
    binary_picture: bytes = Column(LargeBinary, nullable=False) 
