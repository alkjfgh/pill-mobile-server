from sqlalchemy.orm import Session
from app.models.user import User
from app.services.base import BaseService
from app.models.userDto import UserLoginData


class UserService(BaseService[User]):
    def __init__(self, db: Session):
        super().__init__(User, db)

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(self.model).filter(self.model.email == email).first()

    def create_user(self, user: User) -> bool:
        try:
            self.db.add(user)
            self.db.commit()
            return True
        except Exception as e:
            print(f"Error in create_user: {str(e)}")
            self.db.rollback()
            return False

    def login(self, requestUser: UserLoginData) -> bool:
        user = self.get_by_email(requestUser.email)
        if not user:
            return False
        return user.password == requestUser.password

    def update_user(self, user_id: int, user_data: dict) -> bool:
        return self.update(user_id, user_data)
