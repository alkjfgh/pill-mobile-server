from fastapi import APIRouter, HTTPException, Form, UploadFile, File
from app.services.user_service import UserService
from app.models.log import Log
from app.services.log_service import LogService
import os
from datetime import datetime
from app.db.base_class import db
from datetime import datetime
from fastapi.responses import FileResponse
from app.core.config import settings
from app.services.image_service import ImageService
from app.services.descriptionService import DescriptionService

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
    description: str = Form(...),
):
    print(f"logs create log email:{email}")
    print(f"date: {date}")
    try:
        # 이메일 유효성 검사
        if not email:
            raise HTTPException(status_code=400, detail="이메일이 필요합니다")

        # 사용자 존재 여부 확인
        user_service = UserService(db=db)
        user = user_service.get_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail="존재하지 않는 사용자입니다")

        # 이미지 업로드
        image_service = ImageService()
        file_path = await image_service.upload(image, user)

        # 입력된 날짜를 datetime 객체로 파싱
        parsed_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

        # Log 객체 생성 및 저장
        log = Log(
            email=email,
            image=str(file_path),
            result=result,
            date=parsed_date,
        )
        log_service = LogService(db=db)
        created_log = log_service.create_log(log)
        if not created_log:
            raise HTTPException(
                status_code=500, detail="로그 생성/저장 중 오류가 발생했습니다"
            )

        description_service = DescriptionService(db=db)
        isSuccess = description_service.create_description(created_log.id, description)
        if not isSuccess:
            raise HTTPException(
                status_code=500, detail="설명 생성/저장 중 오류가 발생했습니다"
            )

        return {"message": "로그가 생성되었습니다"}

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"로그 생성 중 오류가 발생했습니다: {str(e)}"
        )


@router.get(
    "/{email}",
    summary="사용자 로그 조회",
    description="주어진 이메일에 해당하는 사용자의 로그를 조회합니다.",
    tags=["logs"],
    responses={
        200: {
            "description": "성공적으로 로그를 조회했습니다.",
            "content": {
                "application/json": {
                    "example": {"message": "Get logs for example@email.com", "logs": []}
                }
            },
        },
        400: {
            "description": "잘못된 요청",
            "content": {
                "application/json": {"example": {"detail": "이메일이 필요합니다"}}
            },
        },
        404: {
            "description": "사용자를 찾을 수 없습니다.",
            "content": {
                "application/json": {
                    "example": {"detail": "존재하지 않는 사용자입니다"}
                }
            },
        },
    },
)
async def get_logs(email: str):
    print("logs get_logs")
    print("email: ", email)
    try:
        if not email:
            raise HTTPException(status_code=400, detail="이메일이 필요합니다")

        user_service = UserService(db=db)
        user = user_service.get_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail="존재하지 않는 사용자입니다")

        log_service = LogService(db=db)
        logs = log_service.get_logs(email)
        description_service = DescriptionService(db=db)

        # 로그 데이터 처리
        processed_logs = []
        for log in logs:
            log_dict = {
                "email": log.email,
                "image": log.image,
                "result": log.result,
                "date": log.date.strftime("%Y-%m-%d %H:%M:%S") if log.date else None,
            }
            if not os.path.exists(log_dict["image"]):
                log_dict["image"] = None

            description = description_service.get_description(log.id)
            log_dict["description"] = description.description
            processed_logs.append(log_dict)
        print("size of processed_logs: ", len(processed_logs))

        return {
            "message": f"Get logs for {email}",
            "logs": processed_logs if processed_logs else [],
        }
    except Exception as e:
        print(f"Error getting logs: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get(
    "/image/{image_path:path}",
    summary="이미지 조회 API",
    description="서버에 저장된 이미지를 조회합니다",
    response_class=FileResponse,
    tags=["logs"],
    responses={
        200: {
            "description": "이미지 파일",
            "content": {"image/*": {}},
        },
        404: {
            "description": "이미지를 찾을 수 없음",
            "content": {
                "application/json": {"example": {"detail": "이미지를 찾을 수 없습니다"}}
            },
        },
    },
)
async def get_image(image_path: str):
    print("logs get_image")
    print("image_path: ", image_path)
    try:
        image_service = ImageService()
        full_path = image_service.get_image(image_path)

        return FileResponse(full_path)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"이미지 조회 중 오류가 발생했습니다: {str(e)}"
        )
