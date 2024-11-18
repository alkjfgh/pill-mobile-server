from sqlalchemy.orm import Session
from app.models.user import User
from app.services.base import BaseService


class UserService(BaseService[User]):
    def __init__(self, db: Session):
        super().__init__(User, db)

    def get_by_email(self, email: str):
        return self.db.query(self.model).filter(self.model.email == email).first()

    def create_user(self, user: User) -> bool:
        try:
            # self.db.session.add 대신 self.db.add 사용
            self.db.add(user)
            self.db.commit()
            return True
        except Exception as e:
            print(f"Error in create_user: {str(e)}")
            self.db.rollback()
            return False

    def update_user(self, user_id: str, user_data: dict):
        # 사용자 업데이트 전 추가 검증이나 비즈니스 로직 수행
        return self.update(user_id, user_data)
