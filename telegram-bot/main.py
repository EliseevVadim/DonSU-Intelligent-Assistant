import asyncio

from aiogram.filters import Command

from aiogram import Dispatcher, Bot, F
from aiogram.types import Message

from config import BOT_TOKEN
from core.assistant_api import check_user_registered, register_user, generate_assistant_response, reset_context
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


@dispatcher.message(Command("clear"))
async def command_start_handler(message: Message) -> None:
    user_id = message.from_user.id
    await reset_context(
        user_id=user_id
    )
    await message.answer(
        "История чата успешно очищена!"
    )


@dispatcher.message(F.text)
async def handle_any_text(message: Message):
    response = generate_assistant_response(message)
    await message.answer(response.get("answer"))


@dispatcher.message(F.sticker)
async def handle_sticker(message: Message):
    await message.answer("К сожалению, я не понимаю значений всех стикеров :[ Давайте продолжим общаться текстом!")


@dispatcher.message(F.photo)
async def handle_photo(message: Message):
    await message.answer(
        "📸 Наверное интересная картинка...но я не понимаю ее. Задайте мне вопрос текстом!")


@dispatcher.message(F.video)
async def handle_video(message: Message):
    await message.answer("🎬 Видео просмотрено и проанализировано..., но я все еще разбираюсь только в тексте.")


@dispatcher.message(F.voice)
async def handle_voice(message: Message):
    await message.answer("К сожалению, расширфровка голосовых является пустой тратой вычислительных "
                         "ресурсов...давайте общаться текстом")


@dispatcher.message(F.video_note)
async def handle_video_note(message: Message):
    await message.answer("🎥 Кружочек проанализирован и сохранен, когда-нибудь я его пойму. "
                         "Но сейчас попробуйте текстом!")


@dispatcher.message(F.audio)
async def handle_audio(message: Message):
    await message.answer("🎧 Интересная запись, но давайте пообщаемся текстом!")


@dispatcher.message(F.document)
async def handle_document(message: Message):
    await message.answer(
        "Пока что я умею работать только с текстом. Спросите меня о чем-нибудь!"
    )


@dispatcher.message(F.animation)
async def handle_animation(message: Message):
    await message.answer("🎞️ Гифку посмотрел, но продолжим общаться текстом!")


@dispatcher.message(F.contact)
async def handle_contact(message: Message):
    await message.answer("📇 Контакт сохранен, но я пока что понимаю только текст!")


@dispatcher.message(F.location)
async def handle_location(message: Message):
    await message.answer("📍 Однажды мы встретимся в этой точке! Но сейчас давайте пообщаемся текстом!")


@dispatcher.message(~F.text)
async def handle_unknown(message: Message):
    await message.answer(
        "🤷 К сожалению, я пока умею понимать только текст. Напишите мне словами, и я постараюсь помочь!"
    )


async def main() -> None:
    logger.info("Бот запускается...")
    bot = Bot(token=BOT_TOKEN)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
