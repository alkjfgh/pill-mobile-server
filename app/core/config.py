from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    PROJECT_NAME: str = "Pill Mobile API"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"

    # Database 설정
    DATABASE_URL: str

    # JWT 설정
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24시간

    # 포트 설정
    PORT: int = 8883

    # 이미지 업로드 경로
    UPLOAD_DIR: str

    @property
    def UPLOAD_DIR_PATH(self) -> str:
        return os.path.expanduser(self.UPLOAD_DIR)

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
