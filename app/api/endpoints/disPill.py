from fastapi import APIRouter, HTTPException, UploadFile, File
from PIL import Image
import io

router = APIRouter()


@router.post(
    "/",
    summary="알약 이미지 판별 API",
    description="업로드된 알약 이미지를 분석하여 알약의 이름을 반환합니다",
    response_description="알약 판별 결과",
    tags=["Pills"],
    responses={
        200: {
            "description": "성공적으로 알약을 판별했을 때의 응답",
            "content": {
                "application/json": {
                    "example": {
                        "message": "알약 이미지 판별 성공",
                        "pill_name": "타이레놀",
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
            image.verify()  # 이미지 파일 검증

            # # 이미지 크기 제한 검사 (선택사항)
            # if image.size[0] > 5000 or image.size[1] > 5000:
            #     raise HTTPException(
            #         status_code=400,
            #         detail="이미지 크기가 너무 큽니다. 5000x5000 이하의 이미지를 업로드해주세요.",
            #     )

        except Exception as e:
            raise HTTPException(
                status_code=400, detail="유효하지 않은 이미지 파일입니다"
            )

        # 여기에 이미지 처리 로직 추가
        pill_name = "알약 이름"
        return {"message": "알약 이미지 판별 성공", "pill_name": pill_name}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
