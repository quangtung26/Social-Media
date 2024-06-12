from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

######################## POSTS ############################
class PostBase(BaseModel):
    
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True


######################## USERS ############################
class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


######################## AUTH ############################
class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None