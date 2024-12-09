from sqlalchemy import Column, String, DateTime, func
from app.db.base_class import Base
import uuid


class Log(Base):
    __tablename__ = "logs"

    id = Column(String(100), primary_key=True)
    date = Column(DateTime, server_default=func.now())
    image = Column(String(255))
    result = Column(String(255))
    email = Column(String(255))

    def __init__(self, date: DateTime, image: str, result: str, email: str):
        self.id = uuid.uuid4()
        self.date = date
        self.image = image
        self.result = result
        self.email = email

    def __str__(self):
        return f"Log(id={self.id}, date={self.date}, image={self.image}, result={self.result}, email={self.email})"
