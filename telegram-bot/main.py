import asyncio

from aiogram.filters import Command

from aiogram import Dispatcher, Bot, F
from aiogram.types import Message

from config import BOT_TOKEN
from core.assistant_api import check_user_registered, register_user, generate_assistant_response
from core.logger import logger

dispatcher = Dispatcher()


@dispatcher.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    user_id = message.from_user.id
    user_exists = await check_user_registered(user_id)
    if not user_exists:
        await register_user(
            user_id=user_id,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name
        )
    await message.answer(
        "🤖 Этот ИИ-ассистент создан для помощи студентам и абитуриентам Донецкого государственного университета.\n\n"
        "⚠️ Пожалуйста, учитывайте, что ответы могут содержать неточности. Всегда перепроверяйте важную информацию, "
        "особенно связанную с расписанием, приёмной комиссией, учебными документами и нормативными актами."
    )


@dispatcher.message(F.text)
async def handle_any_text(message: Message):
    response = generate_assistant_response(message)
    await message.answer(response.get("answer"))


async def main() -> None:
    logger.info("Бот запускается...")
    bot = Bot(token=BOT_TOKEN)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
