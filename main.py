from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import router
from app.core.config import settings


def create_app() -> FastAPI:
    app = FastAPI(
        title="Pill Mobile API", description="Pill Mobile Backend API", version="1.0.0"
    )

    # CORS 설정
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 실제 운영 환경에서는 구체적인 도메인을 지정해야 합니다
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 라우터 등록
    app.include_router(router, prefix="/api")

    return app


app = create_app()
