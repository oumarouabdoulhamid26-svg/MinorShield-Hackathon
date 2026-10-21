
# app/schemas/auth.py

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email    : EmailStr
    password : str = Field(min_length=6, max_length=128)
    name     : str | None = None
    phone    : str | None = None
    fcm_token: str | None = None


class UpdateProfileRequest(BaseModel):
    name : str | None = None
    email: EmailStr


class LoginRequest(BaseModel):
    email   : EmailStr
    password: str


class SetPinRequest(BaseModel):
    pin: str = Field(min_length=4, max_length=6, pattern=r"^\d+$")
    # Obligatoire dès qu'un PIN existe déjà : sans lui, n'importe quelle session
    # ouverte pourrait écraser le PIN parent sans le connaître.
    current_pin: str | None = None


class UpdateFcmTokenRequest(BaseModel):
    fcm_token: str


class VerifyPinRequest(BaseModel):
    pin: str


class VerifyPinResponse(BaseModel):
    valid         : bool
    pin_configured: bool


class TokenResponse(BaseModel):
    access_token  : str
    token_type    : str = "bearer"
    parent_id     : str
    email         : str
    email_verified: bool = True


class NotificationPrefs(BaseModel):
    on_detection : bool = True
    daily_summary: bool = True


class VerifyEmailRequest(BaseModel):
    code: str


class ParentResponse(BaseModel):
    id        : str
    email     : str
    name      : str | None = None
    phone     : str | None = None
    created_at: str
    # Permet à l'app de savoir s'il faut demander le PIN actuel avant de le changer
    pin_configured: bool = False
    email_verified: bool = False

    class Config:
        from_attributes = True
