from pydantic import BaseModel, Field


class CreateApplicationDTO(BaseModel):
    name: str = Field(..., description="Название приложения", min_length=5)
    auth_provider_name: str = Field(..., description="Значение, которое будет указано в качестве источника "
                                                     "авторизации для зарегистрированных пользователей "
                                                     "через приложение", min_length=2)
    description: str = Field(..., description="Описание приложения")


class UpdateApplicationDTO(BaseModel):
    app_key: str = Field(..., description="Ключ приложения")
    name: str = Field(..., description="Название приложения", min_length=5)
    auth_provider_name: str = Field(..., description="Значение, которое будет указано в качестве источника "
                                                     "авторизации для зарегистрированных пользователей "
                                                     "через приложение", min_length=2)
    description: str = Field(..., description="Описание приложения")
