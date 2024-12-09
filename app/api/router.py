from fastapi import APIRouter
from app.api.endpoints import users, disPill, logs

router = APIRouter()

# 사용자 관련 API
router.include_router(users.router, prefix="/users")

# 알약 이미지 판별 관련 API
router.include_router(disPill.router, prefix="/disPill")

# 로그 관련 API
router.include_router(logs.router, prefix="/logs")
