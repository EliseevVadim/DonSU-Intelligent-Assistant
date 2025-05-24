import random

from vkbottle.bot import Bot, Message

from config import VK_API_KEY
from core.assistant_api import check_user_registered, register_user, generate_assistant_response

bot = Bot(VK_API_KEY)


@bot.on.message()
async def on_message(message: Message):
    user_id = message.from_id
    user_exists = await check_user_registered(user_id)
    if not user_exists:
        await register_user(user_id, bot)
    response = generate_assistant_response(message)
    await message.answer(
        message=response.get('answer'),
        random_id=random.randint(0, 2**31 - 1)
    )


bot.run_forever()
