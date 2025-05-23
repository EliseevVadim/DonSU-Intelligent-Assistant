from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserRegistrationDTO(BaseModel):
    first_name: str = Field(..., description="Имя пользователя")
    last_name: str = Field(..., description="Фамилия пользователя")
    email: EmailStr = Field(..., description="Электронная почта")
    password: str = Field(..., min_length=6, description="Пароль, не менее 6 символов")


class ExternalUserRegistrationDTO(BaseModel):
    first_name: str = Field(..., description="Имя пользователя")
    last_name: str = Field(..., description="Фамилия пользователя")
    external_user_id: str = Field(..., description="Id пользователя в стороннем приложении")
    api_key: str = Field(..., description="Токен приложения")


class GetExternalUsersDTO(BaseModel):
    api_key: str = Field(..., description="Токен приложения")


class GetExternalUserRegisteredDTO(BaseModel):
    external_user_id: str = Field(..., description="Id пользователя в стороннем приложении")
    api_key: str = Field(..., description="Токен приложения")


class UserLoginDTO(BaseModel):
    email: EmailStr = Field(..., description="Электронная почта")
    password: str = Field(..., min_length=6, description="Пароль, не менее 6 символов")


class UserPublicDTO(BaseModel):
    id: int = Field(..., description="ID пользователя")
    first_name: str = Field(..., description="Имя пользователя")
    last_name: str = Field(..., description="Фамилия пользователя")
    email: EmailStr = Field(..., description="Электронная почта")
    created_at: datetime = Field(..., description="Дата создания пользователя")
    updated_at: datetime = Field(..., description="Дата обновления информации о пользователе")


class ResetPasswordRequestDTO(BaseModel):
    email: EmailStr = Field(..., description="Электронная почта")


class ResetPasswordDTO(BaseModel):
    token: str
    new_password: str = Field(..., min_length=6)
    confirm_new_password: str = Field(..., min_length=6)

