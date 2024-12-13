from sqlalchemy.orm import Session
from app.models.description import Description
from app.services.base import BaseService
from typing import List
from uuid import UUID


class DescriptionService(BaseService[Description]):
    def __init__(self, db: Session):
        super().__init__(Description, db)

    def create_description(self, description: Description) -> bool:
        print("descriptionService create_description")
        print("description: ", description)
        try:
            self.db.add(description)
            self.db.commit()
            print("descriptionService create_description success")
            return True
        except Exception as e:
            print(f"Error in create_description: {str(e)}")
            self.db.rollback()
            return False

    def get_description(self, id: UUID) -> Description:
        print("descriptionService get_description")
        print("id: ", id)
        try:
            description = self.db.query(self.model).filter(self.model.id == id).first()
            print("descriptionService get_description success")
            return description
        except Exception as e:
            print(f"Error in get_description: {str(e)}")
            return None
