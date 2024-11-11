from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Pill Mobile API"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"

    # Database 설정
    DATABASE_URL: str

    # JWT 설정
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24시간

    # SSL 설정
    SSL_KEYFILE: str = "key.pem"
    SSL_CERTFILE: str = "cert.pem"
    SSL_PORT: int = 8443

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
