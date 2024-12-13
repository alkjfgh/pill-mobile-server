from sqlalchemy.orm import Session
from app.models.log import Log
from app.services.base import BaseService
from typing import List
from uuid import UUID
from app.services.image_service import ImageService


class LogService(BaseService[Log]):
    def __init__(self, db: Session):
        super().__init__(Log, db)
        self.image_service = ImageService()

    def create_log(self, log: Log) -> Log:
        print("logService create_log")
        print("log: ", log)
        try:
            self.db.add(log)
            self.db.commit()
            print("logService create_log success")
            log = self.get_log_by_id(log.id)
            return log
        except Exception as e:
            print(f"Error in create_log: {str(e)}")
            self.db.rollback()
            return None

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

            # 이미지 경로 저장
            image_path = log.image

            # 로그 데이터 삭제
            self.db.delete(log)
            self.db.commit()

            # DB 삭제 성공 후 이미지 삭제
            if image_path:
                self.image_service.delete_image(image_path)

            print("logService delete_log success")
            return log
        except Exception as e:
            print(f"Error in delete_log: {str(e)}")
            self.db.rollback()
            raise e

    def delete_all_logs(self):
        print("logService delete_all_logs")
        try:
            # 모든 로그 데이터 삭제
            self.db.query(self.model).delete()
            self.db.commit()

            # 모든 이미지 파일 삭제
            self.image_service.delete_all_images()
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
