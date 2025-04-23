from langchain_core.messages import HumanMessage, AIMessage

from app.business_logic.messages.enums import MessageSender
from app.business_logic.messages.models import Message


def generate_response(query: str, rag_chain, chat_history: list):
    result = rag_chain.invoke({
        'input': query,
        'chat_history': chat_history
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
