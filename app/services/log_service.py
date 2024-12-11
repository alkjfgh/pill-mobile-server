from sqlalchemy.orm import Session
from app.models.log import Log
from app.services.base import BaseService
from typing import List
from bson import ObjectId
from uuid import UUID

class LogService(BaseService[Log]):
    def __init__(self, db: Session):
        super().__init__(Log, db)

    def create_log(self, log: Log) -> bool:
        print("logService create_log")
        print("log: ", log)
        try:
            self.db.add(log)
            self.db.commit()
            print("logService create_log success")
            return True
        except Exception as e:
            print(f"Error in create_log: {str(e)}")
            self.db.rollback()
            return False

    def get_logs(self, email: str) -> List[Log]:
        print("logService get_logs")
        print("email: ", email)
        try:
            logs = self.db.query(self.model).filter(self.model.email == email).all()
            print("logService get_logs success")
            return logs
        except Exception as e:
            print(f"Error in get_logs: {str(e)}")
            return []

    def delete_log(self, log_id: str):
        print("logService delete_log")
        print("log_id: ", log_id)
        try:
            uuid_obj = UUID(log_id)
            log = self.db.query(self.model).filter(self.model.id == uuid_obj).first()
            if not log:
                raise ValueError("로그를 찾을 수 없습니다")
            self.db.delete(log)
            self.db.commit()
            print("logService delete_log success")
            return log
        except ValueError as ve:
            print(f"ValueError in delete_log: {str(ve)}")
            raise ve
        except Exception as e:
            print(f"Error in delete_log: {str(e)}")
            self.db.rollback()
            raise e

    def delete_all_logs(self):
        print("logService delete_all_logs")
        try:
            self.db.query(self.model).delete()
            self.db.commit()
            print("logService delete_all_logs success")
        except Exception as e:
            self.db.rollback()
            raise e

    def get_log_by_id(self, log_id: str) -> Log:
        print("logService get_log_by_id")
        print("log_id: ", log_id)
        try:
            uuid_obj = UUID(log_id)
            log = self.db.query(self.model).filter(self.model.id == uuid_obj).first()
            print("logService get_log_by_id success")
            return log
        except Exception as e:
            print(f"Error in get_log_by_id: {str(e)}")
            return None
