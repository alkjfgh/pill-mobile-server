from sqlalchemy.orm import Session
from app.models.log import Log
from app.services.base import BaseService
from typing import List


class LogService(BaseService[Log]):
    def __init__(self, db: Session):
        super().__init__(Log, db)

    def create_log(self, log: Log) -> bool:
        print("logService create_log")
        print("log: ", log)
        try:
            self.db.add(log)
            self.db.commit()
            return True
        except Exception as e:
            print(f"Error in create_log: {str(e)}")
            self.db.rollback()
            return False

    def get_logs(self, email: str) -> List[Log]:
        print("logService get_logs")
        print("email: ", email)
        return self.db.query(self.model).filter(self.model.email == email).all()
