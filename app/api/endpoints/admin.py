from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.services.user_service import UserService
from app.services.log_service import LogService
from app.db.base_class import db
from app.models.admin import Admin

admin_router = APIRouter()
templates = Jinja2Templates(directory="templates")
security = HTTPBasic()

# 하드코딩된 관리자 자격 증명
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "wjdqhqhdks"

# verify_admin 함수 수정
async def verify_admin(request: Request):
    if not request.session.get("admin_authenticated"):
        raise HTTPException(
            status_code=303,
            detail="인증이 필요합니다",
            headers={"Location": "/admin/login"},
        )
    return {"username": ADMIN_USERNAME}

@admin_router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(
        "admin/login.html",
        {"request": request}
    )

@admin_router.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if username != ADMIN_USERNAME or password != ADMIN_PASSWORD:
        return RedirectResponse(
            url="/admin/login",
            status_code=303
        )
    # 세션에 로그인 정보 저장
    request.session["admin_authenticated"] = True
    return RedirectResponse(
        url="/admin/dashboard",
        status_code=303
    )

@admin_router.get("/dashboard", response_class=HTMLResponse)
async def admin_dashboard(request: Request, admin: dict = Depends(verify_admin)):
    user_service = UserService(db=db)
    log_service = LogService(db=db)
    
    users = user_service.get_all()
    logs = log_service.get_all()
    
    return templates.TemplateResponse(
        "admin/dashboard.html",
        {
            "request": request,
            "user_count": len(users),
            "log_count": len(logs),
            "admin": admin
        }
    )

@admin_router.get("/users", response_class=HTMLResponse)
async def admin_users(request: Request, admin: dict = Depends(verify_admin)):
    user_service = UserService(db=db)
    users = user_service.get_all()
    
    return templates.TemplateResponse(
        "admin/users.html",
        {
            "request": request,
            "users": users,
            "admin": admin
        }
    )

@admin_router.get("/logs", response_class=HTMLResponse)
async def admin_logs(request: Request, admin: dict = Depends(verify_admin)):
    log_service = LogService(db=db)
    logs = log_service.get_all()
    
    return templates.TemplateResponse(
        "admin/logs.html",
        {
            "request": request,
            "logs": logs,
            "admin": admin
        }
    )

@admin_router.get("/logout")
async def logout(request: Request):
    # 세션에서 인증 정보 제거
    request.session.pop("admin_authenticated", None)
    response = RedirectResponse(
        url="/admin/login",
        status_code=303
    )
    return response