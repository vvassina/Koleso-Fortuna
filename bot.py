import os
import logging
import random
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Получаем токен бота и ID группы из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_CHAT_ID = int(os.getenv("GROUP_CHAT_ID"))  # Например: -1002579006711

# Инициализация бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Призы (45 неудач, 5 выигрышей)
WINNING_PRIZES = [
    "🎁 Скидка 5% на заказ",
    "🎁 Скидка 10% на заказ",
    "🎉 Скидка 20% на заказ от 10к",
    "🎁 Заказ без комиссии",
    "🚚 Бесплатная доставка"
]
PRIZES = ["❌ Не повезло..."] * 45 + WINNING_PRIZES

# Настройка базы данных
conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    attempts INTEGER DEFAULT 0,
    prizes TEXT DEFAULT ""
)''')
conn.commit()

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer(
        "🎡 Привет! Добро пожаловать в *Колесо Фортуны!*\n\n"
        "Ты можешь крутануть колесо *3 раза*.\n"
        "Испытай удачу и забери свой приз!🔥\n\n"
        "Нажми /spin, чтобы начать!",
        parse_mode="Markdown"
    )

@dp.message_handler(commands=["spin"])
async def spin(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username or "Без username"

    # Проверка количества попыток
    cursor.execute("SELECT attempts, prizes FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()

    if row:
        attempts, prizes = row
    else:
        attempts, prizes = 0, ""
        cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
        conn.commit()

    if attempts >= 3:
        await message.answer("😕 Ты уже использовал все 3 попытки.")
        return

    # Выбор случайного приза
    prize = random.choice(PRIZES)

    # Обновляем данные
    new_attempts = attempts + 1
    new_prizes = prizes + f"{prize}\n" if prize != "❌ Не повезло..." else prizes
    cursor.execute(
        "UPDATE users SET attempts = ?, prizes = ? WHERE user_id = ?",
        (new_attempts, new_prizes, user_id)
    )
    conn.commit()

    if prize == "❌ Не повезло...":
        await message.answer("😔 Не в этот раз. Попробуй снова — вдруг повезёт?")
    else:
        prize_text = (
            f"🎉 Поздравляем! Ты выиграл:\n"
            f"*{prize}*\n\n"
            f"❗️ВАЖНО — срок действия твоего подарка до *30.09.2025*, "
            f"успей оформить заказ до этой даты 🤍\n\n"
            f"🔔 Напомни менеджеру @dadmaksi о своём призе при оформлении заказа"
        )
        await message.answer(prize_text, parse_mode="Markdown")

        # Отправка уведомления в группу
        await bot.send_message(
            chat_id=GROUP_CHAT_ID,
            text=f"🎁 @{username} выиграл: {prize}"
        )
