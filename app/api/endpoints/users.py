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


@router.post(
    "/",
    response_model=Dict[str, str],
    summary="사용자 회원가입",
    description="새로운 사용자를 생성합니다. 이메일이 이미 존재하는 경우 생성할 수 없습니다.",
    responses={
        200: {
            "description": "성공적으로 사용자를 생성했습니다.",
            "content": {"application/json": {"example": {"message": "Create user"}}},
        },
        400: {
            "description": "이미 존재하는 사용자입니다.",
            "content": {
                "application/json": {"example": {"detail": "User already exists"}}
            },
        },
        422: {
            "description": "유효하지 않은 요청 데이터입니다.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["body", "email"],
                                "msg": "field required",
                                "type": "value_error.missing",
                            }
                        ]
                    }
                }
            },
        },
        500: {
            "description": "서버 오류로 사용자 생성에 실패했습니다.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Internal server error: Failed to create user"
                    }
                }
            },
        },
    },
)
async def create_user(requestUser: UserLoginData):
    try:
        print("requestUser: ", requestUser)

        user_service = UserService(db=db)
        is_user_exist = user_service.get_by_email(requestUser.email)
        print("is_user_exist: ", is_user_exist)

        if is_user_exist:
            raise HTTPException(status_code=400, detail="User already exists")

        new_user = User(
            uid=requestUser.uid,
            email=requestUser.email,
            display_name=requestUser.display_name,
            photo_url=requestUser.photo_url,
            refresh_token=requestUser.stsTokenManager["refreshToken"],
        )

        is_success = user_service.create_user(new_user)
        print("is_success: ", is_success)

        if not is_success:
            raise HTTPException(status_code=500, detail="Failed to create user")

        return {"message": "Create user"}
    except Exception as e:
        print(f"Error creating user: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post(
    "/login",
    response_model=Dict[str, str],
    summary="사용자 로그인",
    description="사용자 인증을 수행하고 로그인합니다.",
    responses={
        200: {"description": "성공적으로 로그인했습니다."},
        401: {"description": "인증에 실패했습니다."},
    },
)
async def login_user():
    return {"message": "Login user"}


@router.put(
    "/{user_id}",
    response_model=Dict[str, str],
    summary="사용자 정보 수정",
    description="주어진 user_id에 해당하는 사용자의 정보를 수정합니다.",
    responses={
        200: {"description": "성공적으로 사용자 정보를 수정했습니다."},
        404: {"description": "사용자를 찾을 수 없습니다."},
    },
)
async def update_user(user_id: int):
    return {"message": f"Update user {user_id}"}
