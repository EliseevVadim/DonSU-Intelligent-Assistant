from pydantic import BaseModel, Field


class RenameChatDTO(BaseModel):
    chat_id: str = Field(..., description='id чата')
    new_name: str = Field(..., description='Новое название чата')


class ResetChatContextDTO(BaseModel):
    external_user_id: str = Field(..., description='Id пользователя в стороннем приложении')
    api_key: str = Field(..., description="Токен приложения")

