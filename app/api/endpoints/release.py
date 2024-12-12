from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

release_router = APIRouter()
templates = Jinja2Templates(directory="templates")


@release_router.get("/download", response_class=HTMLResponse)
async def download_page(request: Request):
    # 프로젝트 루트 디렉토리의 build 폴더 경로
    build_dir = Path(__file__).parent.parent.parent.parent / "build"

    # APK 파일 찾기
    apk_files = list(build_dir.glob("*_*.*.*.apk"))

    current_version = "0.0.0"
    download_url = ""

    if apk_files:
        # 가장 최신 파일 선택 (수정 시간 기준)
        latest_apk = max(apk_files, key=lambda x: x.stat().st_mtime)

        # 파일 이름에서 버전 추출 (_0.0.0.apk 형식)
        version_str = latest_apk.name.split("_")[-1].replace(".apk", "")
        current_version = version_str

        # 상대 경로로 다운로드 URL 생성
        download_url = f"/build/{latest_apk.name}"

    return templates.TemplateResponse(
        "download.html",
        {
            "request": request,
            "current_version": current_version,
            "download_url": download_url,
            "release_notes": [
                {
                    "version": current_version,
                    "date": "2024-12-12",
                    "notes": ["서버 통신 성공"],
                }
            ],
        },
    )
