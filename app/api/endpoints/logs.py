from fastapi import APIRouter, HTTPException, Form, UploadFile, File
from app.services.user_service import UserService
from app.models.log import Log
from app.services.log_service import LogService
import os
from datetime import datetime
from pathlib import Path
import re
from app.db.base_class import db
from datetime import datetime
import locale

router = APIRouter()


@router.post(
    "/",
    summary="로그 생성 API",
    description="사용자의 알약 판별 결과를 로그로 저장합니다",
    response_description="로그 생성 결과",
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
    print(f"create log email:{email}")
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

        try:
            # 사용자 존재 여부 확인
            user_service = UserService(db=db)
            user = user_service.get_by_email(email)
            if not user:
                raise HTTPException(
                    status_code=404, detail="존재하지 않는 사용자입니다"
                )
        except Exception as e:
            print(f"UserService 오류: {str(e)}")
            raise HTTPException(
                status_code=500, detail=f"사용자 조회 중 오류가 발생했습니다: {str(e)}"
            )

        # 이미지 저장 경로 설정
        upload_dir = os.path.expanduser("~/pill/uploads")
        os.makedirs(upload_dir, exist_ok=True)

        # 고유한 파일명 생성
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_email = re.sub(r"[^a-zA-Z0-9]", "_", email)
        filename = f"{safe_email}_{timestamp}.{file_extension}"
        file_path = Path(upload_dir) / filename

        # 이미지 저장
        with open(file_path, "wb") as f:
            f.write(contents)

        try:
            # 로그 생성 및 저장
            print(f"file_path: {file_path}, type: {type(file_path)}")
            print(f"result: {result}, type: {type(result)}")
            print(f"date: {date}, type: {type(date)}")
            try:
                # 한국어 로케일 설정
                locale.setlocale(locale.LC_TIME, "ko_KR.UTF-8")
                # 입력된 날짜 문자열을 datetime 객체로 변환
                parsed_date = datetime.strptime(date, "%Y. %m. %d. 오후 %I:%M:%S")
                # MySQL datetime 형식으로 변환
                formatted_date = parsed_date.strftime("%Y-%m-%d %H:%M:%S")
            except ValueError as e:
                raise HTTPException(status_code=400, detail="잘못된 날짜 형식입니다")
            log = Log(email=email, image=str(file_path), result=result, date=date)
            print(f"생성된 로그 객체: {log.__dict__}")
            log_service = LogService(db=db)
            isSuccess = log_service.create_log(log)
            if not isSuccess:
                raise HTTPException(
                    status_code=500, detail="로그 생성/저장 중 오류가 발생했습니다"
                )
            print(f"로그 저장 완료")
        except Exception as e:
            print(f"로그 생성/저장 중 오류 발생: {str(e)}")
            print(f"에러 타입: {type(e).__name__}")
            print(f"상세 에러: {e.__dict__}")
            raise HTTPException(
                status_code=500,
                detail=f"로그 생성/저장 중 오류가 발생했습니다: {str(e)}",
            )

        print(10)

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
