from sqlalchemy.orm import Session
from app.models.user import User
from app.services.base import BaseService
from app.models.userDto import UserLoginData


class UserService(BaseService[User]):
    def __init__(self, db: Session):
        super().__init__(User, db)

    def get_by_email(self, email: str) -> User | None:
        print("userService get_by_email")
        print("email: ", email)
        try:
            user = self.db.query(self.model).filter(self.model.email == email).first()
            print("user: ", user)
            return user
        except Exception as e:
            print(f"Error in get_by_email: {str(e)}")
            return None

    def create_user(self, user: User) -> bool:
        print("userService create_user")
        print("user: ", user.email)
        try:
            self.db.add(user)
            self.db.commit()
            return True
        except Exception as e:
            print(f"Error in create_user: {str(e)}")
            self.db.rollback()
            return False

    def login(self, requestUser: UserLoginData) -> bool:
        print("userService login")
        print("requestUser: ", requestUser.email)
        try:
            user = self.get_by_email(requestUser.email)
            if not user:
                return False
            return True
        except Exception as e:
            print(f"Error in login: {str(e)}")
            return False

    def update_user(self, email: str, user_data: dict) -> bool:
        print("userService update_user")
        print("email: ", email)
        print("user_data: ", user_data)
        try:
            user = self.get_by_email(email)
            if not user:
                return False
            return self.update(user, user_data)
        except Exception as e:
            print(f"Error in update_user: {str(e)}")
            self.db.rollback()
            return False

    def delete_user(self, email: str) -> bool:
        print("userService delete_user")
        print("email: ", email)
        try:
            user = self.get_by_email(email)
            if not user:
                return False
            self.db.delete(user)
            self.db.commit()
            print("userService delete user success")
            return True
        except Exception as e:
            print(f"Error in delete_user: {str(e)}")
            self.db.rollback()
            return False
