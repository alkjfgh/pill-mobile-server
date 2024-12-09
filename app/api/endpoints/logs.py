from fastapi import APIRouter, HTTPException, Form, UploadFile, File
from app.services.user_service import UserService
from app.models.log import Log
from app.services.log_service import LogService
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
async def create_log(
    email: str = Form(...),
    image: UploadFile = File(...),
    result: str = Form(...),
    date: str = Form(...),
):
    try:
        # 이메일 유효성 검사
        if not email:
            raise HTTPException(status_code=400, detail="이메일이 필요합니다")

        # 파일 확장자 검사
        ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
        if not image:
            raise HTTPException(status_code=400, detail="이미지 파일이 필요합니다")

        file_extension = image.filename.lower().split(".")[-1]
        if file_extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400, detail="PNG, JPG, JPEG 형식의 이미지 파일만 허용됩니다"
            )

        # 파일 크기 제한 (10MB)
        MAX_FILE_SIZE = 10 * 1024 * 1024
        contents = await image.read(MAX_FILE_SIZE + 1)
        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400, detail="파일 크기는 10MB를 초과할 수 없습니다"
            )

        # 파일 포인터 리셋
        await image.seek(0)

        # 사용자 존재 여부 확인
        user = UserService.get_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail="존재하지 않는 사용자입니다")

        # 프로젝트 루트 디렉토리 기준으로 uploads 폴더 생성
        current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        upload_path = os.path.join(current_dir, 'uploads')
        os.makedirs(upload_path, exist_ok=True)

        # 고유한 파일명 생성
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_email = re.sub(r"[^a-zA-Z0-9]", "_", email)
        filename = f"{safe_email}_{timestamp}.{file_extension}"
        file_path = os.path.join(upload_path, filename)

        # 이미지 저장
        with open(file_path, "wb") as f:
            f.write(contents)

        # 로그 생성 및 저장
        log = Log(email=email, image_path=str(file_path), result=result, date=date)
        LogService.create_log(log)

        return {"message": "로그가 생성되었습니다"}

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"로그 생성 중 오류가 발생했습니다: {str(e)}"
        )


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

        # 이미지 파일 존재 여부 확인 개선
        for log in logs:
            image_path = Path(log.image)
            if not image_path.is_file():
                log.image = None

        return logs

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail="로그 조회 중 오류가 발생했습니다")
