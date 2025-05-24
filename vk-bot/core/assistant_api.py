import aiohttp
import requests
from vkbottle import Bot
from vkbottle.bot import Message

from config import MF_AI_API_KEY, MF_AI_API_URL
from core.logger import logger


async def check_user_registered(user_id: int) -> bool:
    payload = {
        "external_user_id": str(user_id),
        "api_key": MF_AI_API_KEY
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{MF_AI_API_URL}/auth/external-user-registered",
                json=payload,
                timeout=aiohttp.ClientTimeout(total=5)
            ) as response:
                response.raise_for_status()
                data = await response.json()
                return data.get("registered", False)

    except (aiohttp.ClientError, ValueError) as e:
        logger.error(f"[check_user_registered] Ошибка при запросе: {e}")
        return False


async def register_user(user_id: int, vk_client: Bot):
    user_infos = await vk_client.api.users.get(user_ids=[user_id])
    user_info = user_infos[0]
    payload = {
        'first_name': user_info.first_name,
        'last_name': user_info.last_name,
        'external_user_id': str(user_id),
        'api_key': MF_AI_API_KEY
    }
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(f"{MF_AI_API_URL}/auth/register/external", json=payload, timeout=5) as response:
                response.raise_for_status()
        except aiohttp.ClientError as e:
            logger.error(f"[register_user] Ошибка при POST-запросе: {e}")


def generate_assistant_response(message: Message):
    payload = {
        'api_key': MF_AI_API_KEY,
        'external_user_id': str(message.from_id),
        'text_content': message.text
    }
    try:
        response = requests.post(f"{MF_AI_API_URL}/messages/send/external", json=payload)
        response.raise_for_status()
        return response.json().get('response')

    except (requests.RequestException, ValueError) as e:
        logger.error(f"[register_user] Ошибка при запросе: {e}")
