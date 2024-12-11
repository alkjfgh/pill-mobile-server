from sqlalchemy import Column, String, Boolean
from app.db.base_class import Base
from passlib.hash import bcrypt

class Admin(Base):
    __tablename__ = "admins"
    
    username = Column(String(100), primary_key=True)
    password = Column(String(200), nullable=False)
    is_active = Column(Boolean, default=True)

    def verify_password(self, password: str) -> bool:
        return bcrypt.verify(password, self.password)