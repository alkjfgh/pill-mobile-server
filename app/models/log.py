from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from app.db.base_class import Base
import uuid


class Log(Base):
    __tablename__ = "logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date = Column(DateTime, server_default=func.now())
    image = Column(String(255))
    result = Column(String(255))
    email = Column(String(255))

    def __init__(self, date: DateTime, image: str, result: str, email: str):
        self.date = date
        self.image = image
        self.result = result
        self.email = email

    def __str__(self):
        return f"Log(id={self.id}, date={self.date}, result={self.result}, email={self.email})"
