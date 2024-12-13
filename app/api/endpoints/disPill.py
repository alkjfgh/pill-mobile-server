from fastapi import APIRouter, HTTPException, UploadFile, File
from PIL import Image
import io
from app.services.DisImageService import DisImageService
import os
from app.core.pillTrans import PillTrans

router = APIRouter()
disImageService = DisImageService()


@router.post(
    "/flower",
    summary="꽃 이미지 판별 API",
    description="업로드된 꽃 이미지를 분석하여 꽃의 이름을 반환합니다",
    response_description="꽃 판별 결과",
    tags=["disPil"],
    responses={
        200: {
            "description": "성공적으로 꽃을 판별했을 때의 응답",
            "content": {
                "application/json": {
                    "example": {
                        "message": "꽃 이미지 판별 성공",
                        "name": "sunflower",
                        "translated_name": "해바라기",
                    }
                }
            },
        },
        400: {
            "description": "잘못된 이미지 형식",
            "content": {
                "application/json": {
                    "example": {"detail": "유효하지 않은 이미지 파일입니다"}
                }
            },
        },
    },
)
async def disPill(request: UploadFile = File(...)):
    # 확장자 검사
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
    file_extension = request.filename.lower().split(".")[-1]
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400, detail="PNG, JPG, JPEG 형식의 이미지 파일만 허용됩니다"
        )

    try:
        # 파일 내용 읽기
        contents = await request.read()

        # 이미지 파일 유효성 검사
        try:
            image = Image.open(io.BytesIO(contents))
            # 이미지 검증
            image.verify()

            # 새로운 이미지 객체 생성 (verify 후에는 파일을 다시 열어야 함)
            image = Image.open(io.BytesIO(contents))

            # 현재 디렉토리 기준으로 상대 경로 설정
            current_dir = os.path.dirname(os.path.abspath(__file__))
            image_dir = os.path.join(current_dir, "../../../images")
            os.makedirs(image_dir, exist_ok=True)

            image_path = os.path.join(image_dir, request.filename)
            image.save(image_path)

            # 이미지 처리 로직
            name, translated_name = disImageService.predict_image(image_path)

            # 처리 후 이미지 파일 삭제 (선택사항)
            os.remove(image_path)

            return {
                "message": "꽃 이미지 판별 성공",
                "name": name,
                "translated_name": translated_name,
            }

        except Exception as e:
            raise HTTPException(
                status_code=400, detail="유효하지 않은 이미지 파일입니다"
            )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/",
    summary="알약 이미지 판별 API",
    description="업로드된 알약 이미지를 분석하여 알약의 이름을 반환합니다",
    response_description="알약 판별 결과",
    tags=["disPil"],
    responses={
        200: {
            "description": "성공적으로 알약을 판별했을 때의 응답",
            "content": {
                "application/json": {
                    "example": {
                        "message": "알약 이미지 판별 성공",
                        "name": "타이레놀",
                        "description": "1) 중등도-중증의 급ㆍ만성 통증",
                    }
                }
            },
        },
        400: {
            "description": "잘못된 이미지 형식",
            "content": {
                "application/json": {
                    "example": {"detail": "유효하지 않은 이미지 파일입니다"}
                }
            },
        },
    },
)
async def disPill(request: UploadFile = File(...)):
    # 확장자 검사
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
    file_extension = request.filename.lower().split(".")[-1]
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400, detail="PNG, JPG, JPEG 형식의 이미지 파일만 허용됩니다"
        )

    try:
        # 파일 내용 읽기
        contents = await request.read()

        # 이미지 파일 유효성 검사
        try:
            image = Image.open(io.BytesIO(contents))
            # 이미지 검증
            image.verify()

            # 새로운 이미지 객체 생성 (verify 후에는 파일을 다시 열어야 함)
            image = Image.open(io.BytesIO(contents))

            # 현재 디렉토리 기준으로 상대 경로 설정
            current_dir = os.path.dirname(os.path.abspath(__file__))
            image_dir = os.path.join(current_dir, "../../../images")
            os.makedirs(image_dir, exist_ok=True)

            image_path = os.path.join(image_dir, request.filename)
            image.save(image_path)

            # 이미지 처리 로직
            name = disImageService.predict_pill(image_path)

            # 처리 후 이미지 파일 삭제 (선택사항)
            os.remove(image_path)

            pillTrans = PillTrans()
            description = pillTrans.trans(name)

            return {
                "message": "알약 이미지 판별 성공",
                "name": name,
                "description": description,
            }

        except Exception as e:
            raise HTTPException(
                status_code=400, detail="유효하지 않은 이미지 파일입니다"
            )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
