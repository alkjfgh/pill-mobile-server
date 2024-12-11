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
async def admin_logs(
    request: Request, 
    email: str = None,
    admin: dict = Depends(verify_admin)
):
    log_service = LogService(db=db)
    logs = log_service.get_all()
    
    # 이메일 검색 필터링
    if email:
        logs = [log for log in logs if email.lower() in log.email.lower()]
    
    return templates.TemplateResponse(
        "admin/logs.html",
        {
            "request": request,
            "logs": logs,
            "admin": admin,
            "search_email": email
        }
    )

@admin_router.delete("/logs/{log_id}")
async def delete_log(log_id: str, admin: dict = Depends(verify_admin)):
    log_service = LogService(db=db)
    try:
        # UUID에서 하이픈 제거
        formatted_log_id = log_id.replace("-", "")
        
        # 로그가 존재하는지 먼저 확인
        log = log_service.get_log_by_id(formatted_log_id)
        if not log:
            raise HTTPException(
                status_code=404,
                detail="해당 ID의 로그를 찾을 수 없습니다"
            )
            
        log_service.delete_log(formatted_log_id)
        return {"message": "로그가 성공적으로 삭제되었습니다"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"로그 삭제 중 오류가 발생했습니다: {str(e)}"
        )

@admin_router.delete("/logs")
async def delete_all_logs(admin: dict = Depends(verify_admin)):
    log_service = LogService(db=db)
    try:
        log_service.delete_all_logs()
        return {"message": "모든 로그가 성공적으로 삭제되었습니다"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@admin_router.get("/logout")
async def logout(request: Request):
    # 세션에서 인증 정보 제거
    request.session.pop("admin_authenticated", None)
    response = RedirectResponse(
        url="/admin/login",
        status_code=303
    )
    return response

@admin_router.delete("/users/{user_id}")
async def delete_user(email: str, admin: dict = Depends(verify_admin)):
    user_service = UserService(db=db)
    try:
        user_service.delete_user(email)
        return {"message": "사용자가 성공적으로 삭제되었습니다"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@admin_router.put("/users/{user_id}")
async def update_user(
    user_id: str,
    email: str = Form(...),
    display_name: str = Form(...),
    admin: dict = Depends(verify_admin)
):
    user_service = UserService(db=db)
    try:
        user_service.update_user(user_id, {"email": email, "displayName": display_name})
        return {"message": "사용자 정보가 업데이트되었습니다"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))