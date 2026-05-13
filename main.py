import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# =========================
TOKEN = "8729643272:AAEew8aqaiff5zACXp1iXi_OA8fPwMO5V1s"
ADMIN_ID = 5192014741
# =========================

bot = Bot(token=TOKEN)
dp = Dispatcher()

# DATABASE
db = sqlite3.connect("users.db")
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY,
    full_name TEXT,
    paid INTEGER DEFAULT 0
)
""")
db.commit()

# MENU
menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Sportchi qo'shish")],
        [KeyboardButton(text="📋 Sportchilar")],
        [KeyboardButton(text="💰 To'lov qilganlar")],
        [KeyboardButton(text="❌ Qarzdorlar")],
        [KeyboardButton(text="📢 Barchaga xabar")]
    ],
    resize_keyboard=True
)

# START
@dp.message(Command("start"))@dp.message(Command("eslatma"))
async def payment_reminder(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return

    cursor.execute("SELECT id FROM users")
    users = cursor.fetchall()

    text = """
🥊 Umidov Boks Clubi eslatadi!

📅 Oylik to'lov qilish vaqti keldi.
Iltimos to'lovni o'z vaqtida amalga oshiring.

📞 93 283 33 61
"""

    sent = 0
    for user in users:
        try:
            await bot.send_message(user[0], text)
            sent += 1
        except:
            pass

    await message.answer(f"✅ {sent} ta sportchiga yuborildi")
async def start(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer(
            "🥊 Umidov Boks Clubi botiga xush kelibsiz!",
            reply_markup=menu
        )
    else:
        await message.answer("Siz admin emassiz.")

# SPORTCHI QO'SHISH
@dp.message(lambda m: m.text == "➕ Sportchi qo'shish")
async def add_user(message: types.Message):
    await message.answer("Sportchi ism familiyasini yuboring:")

    @dp.message()
    async def save_user(msg: types.Message):
        name = msg.text
        cursor.execute(
            "INSERT INTO users(full_name) VALUES(?)",
            (name,)
        )
        db.commit()
        await msg.answer("✅ Qo'shildi")

# SPORTCHILAR
@dp.message(lambda m: m.text == "📋 Sportchilar")
async def all_users(message: types.Message):
    cursor.execute("SELECT full_name FROM users")
    users = cursor.fetchall()

    if users:
        text = "📋 Sportchilar:\n\n"
        for u in users:
            text += f"• {u[0]}\n"
        await message.answer(text)
    else:
        await message.answer("Sportchi yo'q")

# TO'LOV QILGANLAR
@dp.message(lambda m: m.text == "💰 To'lov qilganlar")
async def paid_users(message: types.Message):
    cursor.execute("SELECT full_name FROM users WHERE paid=1")
    users = cursor.fetchall()

    if users:
        text = "💰 To'lov qilganlar:\n\n"
        for u in users:
            text += f"✅ {u[0]}\n"
        await message.answer(text)
    else:
        await message.answer("Hali yo'q")

# QARZDORLAR
@dp.message(lambda m: m.text == "❌ Qarzdorlar")
async def debtors(message: types.Message):
    cursor.execute("SELECT full_name FROM users WHERE paid=0")
    users = cursor.fetchall()

    if users:
        text = "❌ Qarzdorlar:\n\n"
        for u in users:
            text += f"❌ {u[0]}\n"
        await message.answer(text)
    else:
        await message.answer("Qarzdor yo'q")

# BARCHAGA XABAR
@dp.message(lambda m: m.text == "📢 Barchaga xabar")
async def send_all(message: types.Message):
    await message.answer("Yuboriladigan xabarni kiriting:")

    @dp.message()
    async def send_message(msg: types.Message):
        cursor.execute("SELECT id FROM users")
        users = cursor.fetchall()

        for user in users:
            try:
                await bot.send_message(user[0], msg.text)
            except:
                pass

        await msg.answer("✅ Hammasiga yuborildi")

# RUN
async def main():
    print("Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
