from sqlalchemy import Column, String, DateTime, func, Text
from sqlalchemy.dialects.postgresql import UUID
from app.db.base_class import Base
import uuid


class Description(Base):
    __tablename__ = "descriptions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    description = Column(Text)

    def __init__(self, id: UUID, description: str):
        self.id = id
        self.description = description

    def __str__(self):
        return f"Description(id={self.id}, description={self.description})"
