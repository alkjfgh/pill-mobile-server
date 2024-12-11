from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.api.router import router
from app.core.config import settings
from fastapi_admin.app import app as admin_app
from app.api.endpoints.admin import admin_router

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="알약 이미지 분석 및 판별을 위한 REST API 서버",
        version=settings.VERSION,
        docs_url="/docs",  # Swagger UI URL
        redoc_url="/redoc",  # ReDoc URL
        openapi_url="/openapi.json",  # OpenAPI 스키마
        swagger_ui_parameters={"defaultModelsExpandDepth": -1},  # 모델 섹션 숨기기
        terms_of_service="https://github.com/alkjfgh",
        contact={
            "name": "API Support",
            "url": "https://github.com/alkjfgh",
            "email": "alkfgh@gmail.com",
        },
        license_info={
            "name": "MIT License",
            "url": "https://opensource.org/licenses/MIT",
        },
    )
    
    # CORS 설정
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 정적 파일 설정
    app.mount("/static", StaticFiles(directory="static"), name="static")

    # 관리자 페이지 라우터 등록
    app.include_router(admin_router, prefix="/admin", tags=["admin"])
    
    # API 라우터 등록
    app.include_router(router, prefix="/api")

    return app

app = create_app()
