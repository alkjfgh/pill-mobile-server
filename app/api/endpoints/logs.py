from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from app.db.base_class import db
from app.models.user import User
from app.services.user_service import UserService
from app.models.log import Log
from app.services.log_service import LogService
from app.models.logDto import LogDto
import os
from datetime import datetime
from pathlib import Path
import re

router = APIRouter()


@router.post(
    "/",
    summary="로그 생성 API",
    description="사용자의 알약 판별 결과를 로그로 저장합니다",
    response_description="로그 생성 결과",
    tags=["logs"],
    responses={
        200: {
            "description": "로그가 성공적으로 생성되었을 때의 응답",
            "content": {
                "application/json": {"example": {"message": "로그가 생성되었습니다"}}
            },
        },
        400: {
            "description": "잘못된 요청 또는 이미지 형식",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "PNG, JPG, JPEG 형식의 이미지 파일만 허용됩니다"
                    }
                }
            },
        },
    },
)
async def create_log(logDto: LogDto):
    try:
        # 이메일 유효성 검사
        if not logDto.email:
            raise HTTPException(status_code=400, detail="이메일이 필요합니다")

        # 파일 확장자 검사
        ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
        if not logDto.image:
            raise HTTPException(status_code=400, detail="이미지 파일이 필요합니다")

        file_extension = logDto.image.filename.lower().split(".")[-1]
        if file_extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400, detail="PNG, JPG, JPEG 형식의 이미지 파일만 허용됩니다"
            )

        # 파일 크기 제한 (예: 10MB)
        MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB in bytes
        if await logDto.image.read(MAX_FILE_SIZE + 1):
            await logDto.image.seek(0)  # 파일 포인터 리셋
            raise HTTPException(
                status_code=400, detail="파일 크기는 10MB를 초과할 수 없습니다"
            )
        await logDto.image.seek(0)  # 파일 포인터 다시 리셋

        # 사용자 존재 여부 확인
        user = UserService.get_by_email(logDto.email)
        if not user:
            raise HTTPException(status_code=404, detail="존재하지 않는 사용자입니다")

        # 이미지 저장 경로 설정
        upload_dir = os.getenv("UPLOAD_DIR", "uploads")
        os.makedirs(upload_dir, exist_ok=True)

        # 고유한 파일명 생성
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_email = re.sub(r"[^a-zA-Z0-9]", "_", logDto.email)
        filename = f"{safe_email}_{timestamp}.{file_extension}"
        file_path = Path(upload_dir) / filename

        # 이미지를 청크 단위로 저장
        CHUNK_SIZE = 1024 * 1024  # 1MB 청크 사이즈
        try:
            with open(file_path, "wb") as f:
                while chunk := await logDto.image.read(CHUNK_SIZE):
                    f.write(chunk)
        except Exception as e:
            # 파일 저장 실패시 생성된 파일 삭제
            if file_path.exists():
                file_path.unlink()
            raise HTTPException(status_code=500, detail="이미지 파일 저장 중 오류가 발생했습니다")

        # 로그 생성 및 저장
        log = Log(
            email=logDto.email,
            image_path=str(file_path),
            result=logDto.result,
            date=logDto.date,
        )
        LogService.create_log(log)

        return {"message": "로그가 생성되었습니다"}

    except HTTPException as he:
        raise he
    except IOError as e:
        raise HTTPException(
            status_code=500, detail="이미지 파일 저장 중 오류가 발생했습니다"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="로그 생성 중 오류가 발생했습니다")


@router.get(
    "/{email}",
    summary="사용자 로그 조회 API",
    description="특정 사용자의 모든 알약 판별 기록을 조회합니다",
    response_description="사용자의 로그 목록",
    tags=["logs"],
    responses={
        200: {
            "description": "로그 조회 성공",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "email": "user@example.com",
                            "image_path": "uploads/user_20240320_123456.jpg",
                            "result": "타이레놀",
                            "date": "2024-03-20T12:34:56",
                        }
                    ]
                }
            },
        }
    },
)
async def get_logs(email: str):
    try:
        if not email:
            raise HTTPException(status_code=400, detail="이메일이 필요합니다")

        # 사용자 존재 여부 확인
        user = UserService.get_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail="존재하지 않는 사용자입니다")

        logs = LogService.get_logs(email)
        if not logs:
            return []

        # 이미지 파일 존재 여부 확인 추가
        for log in logs:
            if not os.path.exists(log.image):
                log.image = None  # 또는 기본 이미지 경로

        return logs

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail="로그 조회 중 오류가 발생했습니다")
