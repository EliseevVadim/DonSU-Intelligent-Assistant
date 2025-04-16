from pydantic import BaseModel, Field


class SendMessageDTO(BaseModel):
    chat_id: str = Field(..., description='id чата')
    text_content: str = Field(..., description='Текст сообщения')
