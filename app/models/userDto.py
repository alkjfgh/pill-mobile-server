from pydantic import BaseModel
from typing import Optional


class UserLoginData(BaseModel):
    uid: str
    email: str
    display_name: Optional[str]
    photo_url: Optional[str]
    stsTokenManager: dict  # Firebase 토큰 정보
