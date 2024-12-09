from pydantic import BaseModel
from fastapi import UploadFile, File


class LogDto(BaseModel):
    date: str
    result: str
    email: str
