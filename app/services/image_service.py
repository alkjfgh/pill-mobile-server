import os
from app.core.config import settings
from pathlib import Path
import re
from fastapi import HTTPException, UploadFile
from app.models.user import User
from datetime import datetime

class ImageService:
    def __init__(self):
        self.base_path = os.path.expanduser(settings.UPLOAD_DIR_PATH)

    async def upload(self, image: UploadFile, user: User) -> str:
        print("image_service upload")
        # 이미지 파일 유효성 검사
        if not image or not image.filename:
            raise HTTPException(status_code=400, detail="이미지 파일이 필요합니다")

        # 파일 확장자 검사
        ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
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

        # 이미지 저장 경로 설정
        upload_dir = os.path.expanduser(settings.UPLOAD_DIR_PATH)
        os.makedirs(upload_dir, exist_ok=True)

        # 고유한 파일명 생성
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_email = re.sub(r"[^a-zA-Z0-9]", "_", user.email)
        filename = f"{safe_email}_{timestamp}.{file_extension}"
        file_path = Path(upload_dir) / filename

        # 이미지 저장
        with open(file_path, "wb") as f:
            f.write(contents)

        print("image_service upload end")
        return file_path
    
    def get_image(self, image_path: str) -> str:
        print("image_service get_image")
        full_path = os.path.join(self.base_path, os.path.basename(image_path))
        print("full_path: ", full_path)

        # 파일 존재 여부 확인
        if not os.path.exists(full_path):
            print("이미지를 찾을 수 없습니다")
            raise HTTPException(status_code=404, detail="이미지를 찾을 수 없습니다")
        
        print("image_service get_image end")
        return full_path

    def delete_image(self, image_path: str) -> bool:
        print("image_service delete_image")
        try:
            if not image_path:
                return False
            
            full_path = os.path.join(self.base_path, os.path.basename(image_path))
            print("full_path: ", full_path)
            
            if os.path.exists(full_path):
                os.remove(full_path)
                print(f"이미지 파일 삭제 완료: {full_path}")
                return True
            return False
        except Exception as e:
            print(f"이미지 파일 삭제 실패: {str(e)}")
            return False

    def delete_all_images(self) -> bool:
        print("image_service delete_all_images")
        try:
            # 디렉토리가 존재하는지 확인
            if not os.path.exists(self.base_path):
                return False
            
            # 디렉토리 내의 모든 파일 삭제
            for filename in os.listdir(self.base_path):
                file_path = os.path.join(self.base_path, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            print(f"모든 이미지 파일 삭제 완료: {self.base_path}")
            return True
        except Exception as e:
            print(f"이미지 파일 삭제 실패: {str(e)}")
            return False