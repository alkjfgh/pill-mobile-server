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
        user = self.db.query(self.model).filter(self.model.email == email).first()
        print("user: ", user)
        if user:
            return {
                "uid": user.uid,
                "email": user.email,
                "displayName": user.displayName,
                "photoURL": user.photoURL,
                "createdAt": user.createdAt,
                "lastLoginAt": user.lastLoginAt,
                "refreshToken": user.refreshToken,
            }
        return None

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
        return True

    def update_user(self, email: str, user_data: dict) -> bool:
        user = self.get_by_email(email)
        if not user:
            return False
        return self.update(user, user_data)

    def delete_user(self, email: str) -> bool:
        user = self.get_by_email(email)
        if not user:
            return False
        self.db.delete(user)
        self.db.commit()
        return True
