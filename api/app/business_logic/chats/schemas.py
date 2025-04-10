from pydantic import BaseModel, Field


class RenameChatDTO(BaseModel):
    chat_id: str = Field(..., description='id чата')
    new_name: str = Field(..., description='Новое название чата')
