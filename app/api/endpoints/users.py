from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/{user_id}")
async def get_user(user_id: int):
    return {"message": f"Get user {user_id}"}


@router.post("/")
async def create_user():
    return {"message": "Create user"}


@router.put("/{user_id}")
async def update_user(user_id: int):
    return {"message": f"Update user {user_id}"}
