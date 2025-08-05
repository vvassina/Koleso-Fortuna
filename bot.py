import logging
import random
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import Throttled
from collections import defaultdict
import os

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
user_attempts = defaultdict(int)

prizes = [
    "❌ Не повезло...", "❌ Не повезло...", "❌ Не повезло...", "❌ Не повезло...",
    "🎁 Скидка 5% на заказ", "❌ Не повезло...", "🎁 Скидка 10% на заказ", "❌ Не повезло...",
    "❌ Не повезло...", "🎉 Скидка 20% на заказ от 10к", "❌ Не повезло...", "❌ Не повезло...",
    "❌ Не повезло...", "🎁 Заказ без комиссии", "❌ Не повезло...", "❌ Не повезло...",
    "❌ Не повезло...", "❌ Не повезло...", "❌ Не повезло...", "🚚 Бесплатная доставка"
] + ["❌ Не повезло..."] * 30  # всего 50 призов

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.reply(
        "🎡 Привет! Добро пожаловать в *Колесо Фортуны!*\n\n"
        "Ты можешь крутануть колесо *3 раза*.\n"
        "Испытай удачу и забери свой приз!🔥\n\n"
        "Нажми /spin чтобы попробовать 🍀",
        parse_mode="Markdown"
    )

@dp.message_handler(commands=['spin'])
async def spin_handler(message: types.Message):
    user_id = message.from_user.id
    if user_attempts[user_id] >= 3:
        await message.reply("⛔️ У тебя закончились попытки. Ты уже использовал все 3 прокрута.")
        return

    prize = random.choice(prizes)
    user_attempts[user_id] += 1

    if "❌" in prize:
        await message.reply(f"🎡 Крутим колесо...\n\n{prize}")
    else:
        await message.reply(
            f"🎉 Поздравляем! Ты выиграл:\n{prize}\n\n"
            "❗️*ВАЖНО* — срок действия твоего подарка до *30.09.2025*, успей оформить заказ до этой даты 🤍\n\n"
            "Напомни менеджеру @dadmaksi о своём призе при оформлении заказа.",
            parse_mode="Markdown"
        )

        if CHAT_ID:
            try:
                await bot.send_message(
                    CHAT_ID,
                    f"🎉 Пользователь @{message.from_user.username or message.from_user.full_name} "
                    f"выиграл: {prize}"
                )
            except Exception as e:
                logging.warning(f"Не удалось отправить в чат: {e}")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
