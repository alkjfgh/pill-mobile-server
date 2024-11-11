from fastapi import APIRouter, HTTPException
from typing import Dict

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
async def create_user():
    return {"message": "Create user"}


@router.put("/{user_id}")
async def update_user(user_id: int):
    return {"message": f"Update user {user_id}"}
