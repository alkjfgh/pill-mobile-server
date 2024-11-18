from fastapi import APIRouter, HTTPException
from typing import Dict
from app.db.base_class import db
from app.models.user import User
from app.models.userDto import UserLoginData
from app.services.user_service import UserService

router = APIRouter()


@router.get(
    "/{user_id}",
    response_model=Dict[str, str],
    summary="사용자 정보 조회",
    description="주어진 user_id에 해당하는 사용자의 정보를 조회합니다.",
    responses={
        200: {"description": "성공적으로 사용자 정보를 조회했습니다."},
        404: {"description": "사용자를 찾을 수 없습니다."},
    },
)
async def get_user(user_id: int):
    return {"message": f"Get user {user_id}"}


@router.post("/")
async def create_user(requestUser: UserLoginData):
    response_model = {"message": "Create user"}
    summary = "사용자 생성"
    description = "주어진 사용자 정보를 생성합니다."
    responses = {
        200: {"description": "성공적으로 사용자를 생성했습니다."},
        400: {"description": "잘못된 요청입니다."},
    }

    user_service = UserService(db=db)
    is_user_exist = user_service.get_by_email(requestUser.email)
    if is_user_exist:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(requestUser)
    is_success = user_service.create_user(new_user)
    if not is_success:
        raise HTTPException(status_code=500, detail="Failed to create user")

    return response_model


@router.post("/login")
async def login_user():
    return {"message": "Login user"}


@router.put("/{user_id}")
async def update_user(user_id: int):
    return {"message": f"Update user {user_id}"}
