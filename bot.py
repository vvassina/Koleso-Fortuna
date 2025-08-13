import logging
import random
from aiogram import Bot, Dispatcher, types
from collections import defaultdict
import os
import asyncio
from aiohttp import web

# --- Настройки ---
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")  # ID группы

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
user_attempts = defaultdict(int)

# --- Список призов (50 элементов, шанс выигрыша ≈ 10%) ---
prizes = [
    "❌ Не повезло...",
    "❌ Не повезло...",
    "❌ Не повезло...",
    "❌ Не повезло...",
    "🎁 Скидка 5% на заказ",
    "❌ Не повезло...",
    "🎁 Скидка 10% на заказ",
    "❌ Не повезло...",
    "❌ Не повезло...",
    "🎉 Скидка 20% на заказ от 20к",
    "❌ Не повезло...",
    "❌ Не повезло...",
    "❌ Не повезло...",
    "🎁 Заказ без комиссии",
    "❌ Не повезло...",
    "❌ Не повезло...",
    "❌ Не повезло...",
    "❌ Не повезло...",
    "❌ Не повезло...",
    "🚚 Бесплатная доставка",
    "❌ Не повезло...",
    "❌ Не повезло...",
    "❌ Не повезло...",
    "❌ Не повезло...",
    "❌ Не повезло...",
    "🎉Скидка на комиссию 50%",
    "❌ Не повезло...",
    "❌ Не повезло...",
    "❌ Не повезло...",
    "❌ Не повезло...",
    "❌ Не повезло...",
    "🎉Скидка на комиссию 50%",
    "❌ Не повезло...",
    "🎉Скидка на комиссию 50%",
    "❌ Не повезло...",
    "❌ Не повезло...",
    "❌ Не повезло...",
    "🎁 Заказ без комиссии",
    "❌ Не повезло...",
    "❌ Не повезло...",
    "❌ Не повезло...",
    "❌ Не повезло...",
    "❌ Не повезло...",
    "❌ Не повезло...",
    "❌ Не повезло...",
    "❌ Не повезло...",
    "❌ Не повезло...",
    "🎁 Заказ без комиссии",
    "❌ Не повезло...",
    "❌ Не повезло..."
]

# --- Команды бота ---
@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.reply(
        """🎡 Привет! Добро пожаловать в *Колесо Фортуны!*

Ты можешь крутануть колесо *3 раза*.
Испытай удачу и забери свой приз!🔥

Нажми /spin чтобы попробовать 🍀""",
        parse_mode="Markdown"
    )

@dp.message_handler(commands=['spin'])
async def spin_handler(message: types.Message):
    user_id = message.from_user.id
    if user_attempts[user_id] >= 3:
        await message.reply("⛔️ У тебя закончились попытки. Ты уже использовал все 3 прокрута.")
        return

@dp.message_handler(commands=['ping'])
async def ping_handler(message: types.Message):
    await message.reply("🏓 Pong! Бот на связи.")

    prize = random.choice(prizes)
    user_attempts[user_id] += 1

    if "❌" in prize:
        await message.reply(f"🎡 Крутим колесо...\n\n{prize}")
    else:
        await message.reply(
            f"🎉 Поздравляем! Ты выиграл:\n{prize}\n\n"
            "❗️*ВАЖНО* — срок действия твоего подарка до *30.09.2025*.\n"
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

# --- WEB SERVER ---
async def handle(request):
    return web.Response(text="Bot is running")

async def start_webserver():
    app = web.Application()
    app.add_routes([web.get('/', handle)])
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()

# --- Запуск бота и веб-сервера ---
async def main():
    logging.basicConfig(level=logging.INFO)
    await asyncio.gather(
        start_webserver(),
        dp.start_polling()
    )

if __name__ == '__main__':
    asyncio.run(main())
