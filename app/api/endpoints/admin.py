from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
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

def verify_admin(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != ADMIN_USERNAME or credentials.password != ADMIN_PASSWORD:
        raise HTTPException(
            status_code=401,
            detail="인증 실패",
            headers={"WWW-Authenticate": "Basic"},
        )
    return {"username": ADMIN_USERNAME}

@admin_router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(
        "admin/login.html",
        {"request": request}
    )

@admin_router.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    if username != ADMIN_USERNAME or password != ADMIN_PASSWORD:
        return RedirectResponse(
            url="/admin/login",
            status_code=303
        )
    return RedirectResponse(
        url="/admin/dashboard",
        status_code=303
    )

@admin_router.get("/dashboard", response_class=HTMLResponse)
async def admin_dashboard(request: Request, admin: Admin = Depends(verify_admin)):
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
async def admin_users(request: Request):
    user_service = UserService(db=db)
    users = user_service.get_all()
    
    return templates.TemplateResponse(
        "admin/users.html",
        {
            "request": request,
            "users": users
        }
    )

@admin_router.get("/logs", response_class=HTMLResponse)
async def admin_logs(request: Request):
    log_service = LogService(db=db)
    logs = log_service.get_all()
    
    return templates.TemplateResponse(
        "admin/logs.html",
        {
            "request": request,
            "logs": logs
        }
    )