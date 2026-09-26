from fastapi import APIRouter, HTTPException

from app.core.security import create_access_token
from app.database.schemas import LoginRequest, RegisterRequest, ResetRequest
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
def register(request: RegisterRequest):
    if len(request.password) < 8:
        raise HTTPException(400, "Password must be at least 8 characters")
    try:
        user = auth_service.register(request.username, request.email, request.password)
    except ValueError as exc:
        raise HTTPException(409, str(exc))
    user["access_token"] = create_access_token(user["id"], user["email"])
    return user


@router.post("/login")
def login(request: LoginRequest):
    user = auth_service.login(request.email, request.password)
    if not user:
        raise HTTPException(401, "Invalid email or password")
    return user


@router.get("/me")
def me():
    return {"message": "Use the authenticated user endpoint through the frontend session."}


@router.post("/forgot-password")
def forgot_password(request: dict):
    result = auth_service.create_reset_code(request.get("email", ""))
    if not result:
        raise HTTPException(404, "No account found with this email")
    # Email delivery is intentionally kept behind the API boundary. The code
    # is returned only for local development/testing; production should send it
    # through the backend SMTP service and remove this field.
    return {"message": "Reset code created", "reset_code": result["code"]}


@router.post("/reset-password")
def reset_password(request: ResetRequest):
    if len(request.new_password) < 8:
        raise HTTPException(400, "Password must be at least 8 characters")
    if not auth_service.reset_password(request.email, request.code, request.new_password):
        raise HTTPException(400, "Invalid or expired reset code")
    return {"message": "Password reset successfully"}
