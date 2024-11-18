from sqlalchemy import Column, String, DateTime, func
from app.db.base_class import Base
from app.models.userDto import UserLoginData


class User(Base):
    __tablename__ = "users"

    uid = Column(String(100), primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    displayName = Column(String(100))
    photoURL = Column(String(255))
    createdAt = Column(DateTime, server_default=func.now())
    lastLoginAt = Column(DateTime, onupdate=func.now())
    refreshToken = Column(String(500))

    def __init__(
        self,
        uid: str,
        email: str,
        display_name: str = None,
        photo_url: str = None,
        refresh_token: str = None,
    ):
        self.uid = uid
        self.email = email
        self.displayName = display_name
        self.photoURL = photo_url
        self.refreshToken = refresh_token
