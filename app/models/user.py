from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from app.models.userDto import UserLoginData

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    uid = Column(String(100), primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    displayName = Column(String(100))
    photoURL = Column(String(255))
    createdAt = Column(DateTime, server_default=func.now())
    lastLoginAt = Column(DateTime, onupdate=func.now())
    refreshToken = Column(String(500))

    def __init__(self, user: UserLoginData):
        self.uid = user.uid
        self.email = user.email
        self.displayName = user.display_name
        self.photoURL = user.photo_url
        self.refreshToken = user.stsTokenManager["refreshToken"]
