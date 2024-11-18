from typing import Generic, TypeVar, Type
from sqlalchemy.orm import Session
from app.db.base_class import Base

# 제네릭 타입 변수 정의: Base 클래스를 상속받는 모든 모델 타입에 대해 사용 가능
ModelType = TypeVar("ModelType", bound=Base)


class BaseService(Generic[ModelType]):
    """
    모든 서비스 클래스의 기본이 되는 베이스 서비스 클래스

    제네릭을 사용하여 다양한 모델 타입에 대해 CRUD 작업을 수행할 수 있습니다.

    Attributes:
        model (Type[ModelType]): 서비스가 처리할 SQLAlchemy 모델 클래스
        db (Session): SQLAlchemy 데이터베이스 세션 객체
    """

    def __init__(self, model: Type[ModelType], db: Session) -> None:
        """
        베이스 서비스 초기화

        Args:
            model: 처리할 SQLAlchemy 모델 클래스
            db: 데이터베이스 세션 객체
        """
        self.model = model
        self.db = db

    def get(self, id: str) -> ModelType | None:
        """
        ID로 단일 객체를 조회합니다.

        Args:
            id: 조회할 객체의 고유 식별자

        Returns:
            찾은 객체 또는 None
        """
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_all(self) -> list[ModelType]:
        """
        모든 객체를 조회합니다.

        Returns:
            모델 객체들의 리스트
        """
        return self.db.query(self.model).all()

    def create(self, obj_in: dict) -> ModelType:
        """
        새로운 객체를 생성합니다.

        Args:
            obj_in: 생성할 객체의 데이터를 담은 딕셔너리

        Returns:
            생성된 모델 객체
        """
        obj = self.model(**obj_in)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, id: str, obj_in: dict) -> ModelType | None:
        """
        기존 객체를 업데이트합니다.

        Args:
            id: 업데이트할 객체의 고유 식별자
            obj_in: 업데이트할 데이터를 담은 딕셔너리

        Returns:
            업데이트된 객체 또는 None (객체를 찾지 못한 경우)
        """
        obj = self.get(id)
        if obj:
            for key, value in obj_in.items():
                setattr(obj, key, value)
            self.db.commit()
            self.db.refresh(obj)
        return obj

    def delete(self, id: str) -> ModelType | None:
        """
        객체를 삭제합니다.

        Args:
            id: 삭제할 객체의 고유 식별자

        Returns:
            삭제된 객체 또는 None (객체를 찾지 못한 경우)
        """
        obj = self.get(id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
        return obj
