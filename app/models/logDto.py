from pydantic import BaseModel
from fastapi import UploadFile, File


class LogDto(BaseModel):
    date: str
    image: UploadFile = File(...)
    result: str
    email: str
