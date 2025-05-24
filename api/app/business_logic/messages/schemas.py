from pydantic import BaseModel, Field


class SendMessageDTO(BaseModel):
    chat_id: str = Field(..., description='id чата')
    text_content: str = Field(..., description='Текст сообщения')


class SendMessageExternallyDTO(BaseModel):
    external_user_id: str = Field(..., description="Id пользователя в стороннем приложении")
    api_key: str = Field(..., description="Токен приложения")
    text_content: str = Field(..., description='Текст сообщения')
