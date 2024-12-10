from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from app.db.base_class import db
from app.models.user import User
from app.models.userDto import UserLoginData
from app.services.user_service import UserService

router = APIRouter()


@router.get(
    "/{email}",
    response_model=Dict[str, Any],
    summary="사용자 정보 조회",
    description="주어진 user_id에 해당하는 사용자의 정보를 조회합니다.",
    tags=["users"],
    responses={
        200: {
            "description": "성공적으로 사용자 정보를 조회했습니다.",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Get user example@email.com",
                        "user": {
                            "email": "example@email.com",
                            "display_name": "Example User",
                            "photo_url": "https://example.com/photo.jpg",
                        },
                    }
                }
            },
        },
        404: {
            "description": "사용자를 찾을 수 없습니다.",
            "content": {
                "application/json": {
                    "example": {"detail": "사용자를 찾을 수 없습니다."}
                }
            },
        },
        500: {
            "description": "서버 오류로 사용자 정보를 조회할 수 없습니다.",
            "content": {
                "application/json": {
                    "example": {"detail": "Internal server error: Failed to get user"}
                }
            },
        },
    },
)
async def get_user(email: str):
    print("users get_user")
    print("email: ", email)
    try:
        user_service = UserService(db=db)
        user = user_service.get_by_email(email)
        if user is None:
            raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

        user_dict = {
            "email": user.email,
            "displayName": user.displayName,
            "photoURL": user.photoURL,
            "uid": user.uid,
            "createdAt": user.createdAt.isoformat() if user.createdAt else None,
            "lastLoginAt": user.lastLoginAt.isoformat() if user.lastLoginAt else None,
        }

        return {"message": f"Get user {email}", "user": user_dict}
    except Exception as e:
        print(f"Error getting user: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post(
    "/",
    response_model=Dict[str, str],
    summary="사용자 회원가입",
    description="새로운 사용자를 생성합니다. 이메일이 이미 존재하는 경우 생성할 수 없습니다.",
    tags=["users"],
    responses={
        200: {
            "description": "성공적으로 사용자를 생성했습니다.",
            "content": {
                "application/json": {"example": {"message": "Create user {email}"}}
            },
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

        return {"message": f"Create user {new_user.email}"}
    except Exception as e:
        print(f"Error creating user: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post(
    "/login",
    response_model=Dict[str, str],
    summary="사용자 로그인",
    description="사용자 인증을 수행하고 로그인합니다.",
    tags=["users"],
    responses={
        200: {
            "description": "성공적으로 로그인했습니다.",
            "content": {
                "application/json": {
                    "example": {"message": "Login user example@email.com"}
                }
            },
        },
        401: {
            "description": "인증에 실패했습니다.",
            "content": {
                "application/json": {"example": {"detail": "인증에 실패했습니다."}}
            },
        },
        500: {
            "description": "서버 오류로 로그인에 실패했습니다.",
            "content": {
                "application/json": {
                    "example": {"detail": "Internal server error: Failed to login"}
                }
            },
        },
    },
)
async def login_user(requestUser: UserLoginData):
    try:
        user_service = UserService(db=db)
        is_success = user_service.login(requestUser)
        if not is_success:
            raise HTTPException(status_code=401, detail="인증에 실패했습니다.")

        return {"message": f"Login user {requestUser.email}"}
    except Exception as e:
        print(f"Error logging in: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post(
    "/update",
    response_model=Dict[str, str],
    summary="사용자 정보 수정",
    description="주어진 이메일에 해당하는 사용자의 정보를 수정합니다. 수정 가능한 필드: display_name, photo_url",
    tags=["users"],
    responses={
        200: {
            "description": "성공적으로 사용자 정보를 수정했습니다.",
            "content": {
                "application/json": {
                    "example": {"message": "Update user example@email.com"}
                }
            },
        },
        404: {
            "description": "사용자를 찾을 수 없습니다.",
            "content": {
                "application/json": {
                    "example": {"detail": "사용자를 찾을 수 없습니다."}
                }
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
            "description": "서버 오류로 사용자 정보를 수정할 수 없습니다.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Internal server error: Failed to update user"
                    }
                }
            },
        },
    },
)
async def update_user(email: str, user_data: dict):
    try:
        user_service = UserService(db=db)
        is_success = user_service.update_user(email, user_data)
        if not is_success:
            raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

        return {"message": f"Update user {email}"}
    except Exception as e:
        print(f"Error updating user: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.delete(
    "/{email}",
    response_model=Dict[str, str],
    summary="사용자 삭제",
    description="주어진 이메일에 해당하는 사용자를 삭제합니다.",
    tags=["users"],
    responses={
        200: {
            "description": "성공적으로 사용자를 삭제했습니다.",
            "content": {
                "application/json": {
                    "example": {"message": "Delete user example@email.com"}
                }
            },
        },
        404: {
            "description": "사용자를 찾을 수 없습니다.",
            "content": {
                "application/json": {
                    "example": {"detail": "사용자를 찾을 수 없습니다."}
                }
            },
        },
        500: {
            "description": "서버 오류로 사용자를 삭제할 수 없습니다.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Internal server error: Failed to delete user"
                    }
                }
            },
        },
    },
)
async def delete_user(email: str):
    try:
        user_service = UserService(db=db)
        is_success = user_service.delete_user(email)
        if not is_success:
            raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

        return {"message": f"Delete user {email}"}
    except Exception as e:
        print(f"Error deleting user: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
