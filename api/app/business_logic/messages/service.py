from datetime import date, datetime, timezone, timedelta

from langchain_core.messages import HumanMessage, AIMessage

from app.business_logic.messages.enums import MessageSender
from app.business_logic.messages.models import Message


def generate_response(query: str, rag_chain, chat_history: list):
    result = rag_chain.invoke({
        'input': query,
        'chat_history': chat_history,
        'current_date': date.today().strftime("%d.%m.%Y")
    })
    return result


def build_chat_history(history: list[Message]):
    chat_history = []
    for message in history:
        match message.sender:
            case MessageSender.HUMAN:
                chat_history.append(HumanMessage(content=message.text_content))
            case MessageSender.AI:
                chat_history.append(AIMessage(content=message.text_content))
            case _:
                raise ValueError(f'Unknown sender: {message.sender}')
    return chat_history


def should_clear_context(history: list[Message], hours: int) -> bool:
    if not history:
        return False
    last_message_sent_at = history[-1].created_at
    now = datetime.now(timezone.utc)
    return last_message_sent_at.date() != now.date() and (now - last_message_sent_at > timedelta(hours=hours))
