# -*- coding: utf-8 -*-
from fastapi import APIRouter, HTTPException

from app.core.config import settings
from app.core.security import create_access_token
from app.database.schemas import LoginRequest, RegisterRequest, ResetRequest
from app.services import auth_service
from app.services.email_service import send_password_reset_email

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
    email = request.get("email", "").strip()
    if not email:
        raise HTTPException(400, "Email address is required")

    result = auth_service.create_reset_code(email)
    if not result:
        raise HTTPException(404, "No account found with this email")

    sent, error_msg = send_password_reset_email(
        to_email=result["email"],
        username=result["username"],
        reset_code=result["code"],
    )
    if not sent and settings.sender_email:
        raise HTTPException(500, f"Failed to send reset email: {error_msg}")

    return {"message": "Password reset code sent to your registered email address"}


@router.post("/reset-password")
def reset_password(request: ResetRequest):
    if len(request.new_password) < 8:
        raise HTTPException(400, "Password must be at least 8 characters")
    if not auth_service.reset_password(request.email, request.code, request.new_password):
        raise HTTPException(400, "Invalid or expired reset code")
    return {"message": "Password reset successfully"}
