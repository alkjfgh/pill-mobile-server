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
        allow_origins=["*"],  # 실제 프론트엔드 도메인
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["*"],
    )

    # 라우터 등록
    app.include_router(router, prefix="/api")

    return app


app = create_app()
