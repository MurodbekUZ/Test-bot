"""
Aiogram 3.22 asosida Matematika Test Bot
Foydalanuvchi fullname va natija ADMIN ga yuboriladi
"""

import os
import asyncio
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# 🔑 Token endi atrof-muhit o'zgaruvchisidan olinadi (BOT_TOKEN)
TOKEN = os.getenv("8124923431:AAFfhZpw-uZtcVoYvkmH6PR9e30295ma_Yo")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable is not set")

# 👑 Admin (bot egasi) ID
ADMIN_ID = 6320728801   # o'zingizning Telegram ID raqamingizni yozing

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Foydalanuvchi ma'lumotlari
user_data = {}

# Savol generatori (30 ta savol)
def generate_questions(num=30):
    questions = []
    operations = ["+", "-", "*", "/"]
    for _ in range(num):
        a = random.randint(5, 50)
        b = random.randint(2, 20)
        op = random.choice(operations)

        if op == "+":
            ans = a + b
        elif op == "-":
            ans = a - b
        elif op == "*":
            ans = a * b
        else:  # bo‘lish
            a = a * b
            ans = a // b
            op = "/"

        wrong1 = ans + random.randint(1, 5)
        wrong2 = ans - random.randint(1, 5)
        options = [ans, wrong1, wrong2]
        random.shuffle(options)

        questions.append({
            "q": f"{a} {op} {b} = ?",
            "options": [str(o) for o in options],
            "answer": options.index(ans)
        })
    return questions


def get_keyboard(q_index: int, questions):
    buttons = []
    for i, opt in enumerate(questions[q_index]["options"]):
        buttons.append([InlineKeyboardButton(text=opt, callback_data=f"{q_index}:{i}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# /start komandasi
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    fullname = message.from_user.full_name
    username = f"@{message.from_user.username}" if message.from_user.username else "yo‘q"
    await message.answer(
        "👋 Salom! Men Test Botman.\n"
        "Matematika testini boshlash uchun /test yozing.\n"
        "Qo‘shimcha yordam uchun /help buyrug‘ini bering."
    )
    # Adminni ogohlantirish
    await bot.send_message(
        ADMIN_ID,
        f"📥 Yangi foydalanuvchi start bosdi!\n\n"
        f"👤 Fullname: {fullname}\n"
        f"🆔 ID: {message.from_user.id}\n"
        f"🔗 Username: {username}"
    )


# /help komandasi
@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "ℹ️ Botdan foydalanish yo‘riqnomasi:\n\n"
        "/start – Botni ishga tushirish\n"
        "/help – Yordam\n"
        "/test – 30 ta savollik matematika testini boshlash\n\n"
        "✅ Test tugagach, sizning natijangiz foiz hisobida chiqadi."
    )


# /test komandasi
@dp.message(Command("test"))
async def cmd_test(message: types.Message):
    user_id = message.from_user.id
    questions = generate_questions(30)

    user_data[user_id] = {"score": 0, "current": 0, "questions": questions}

    q = questions[0]
    await message.answer(
        f"Savol 1/{len(questions)}:\n{q['q']}",
        reply_markup=get_keyboard(0, questions)
    )

    # Adminni ogohlantirish
    fullname = message.from_user.full_name
    username = f"@{message.from_user.username}" if message.from_user.username else "yo‘q"
    await bot.send_message(
        ADMIN_ID,
        f"📝 {fullname} (ID: {user_id}, {username}) testni boshladi."
    )


# Javoblarni qayta ishlash
@dp.callback_query(F.data)
async def process_answer(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    if user_id not in user_data:
        await callback.answer("Avval /test buyrug‘ini bering.", show_alert=True)
        return

    data = user_data[user_id]
    q_index, opt_index = map(int, callback.data.split(":"))
    questions = data["questions"]
    correct = questions[q_index]["answer"]

    if opt_index == correct:
        data["score"] += 1
        await callback.answer("✅ To‘g‘ri!")
    else:
        correct_text = questions[q_index]["options"][correct]
        await callback.answer(f"❌ Noto‘g‘ri! To‘g‘ri javob: {correct_text}")

    data["current"] += 1
    next_q = data["current"]

    if next_q < len(questions):
        q = questions[next_q]
        await callback.message.answer(
            f"Savol {next_q+1}/{len(questions)}:\n{q['q']}",
            reply_markup=get_keyboard(next_q, questions)
        )
    else:
        score = data["score"]
        total = len(questions)
        percent = round((score / total) * 100)

        if percent >= 80:
            status = "✅ Siz testdan o‘tdingiz!"
        else:
            status = "❌ Siz testdan o‘tolmadingiz!"

        await callback.message.answer(
            f"📊 Test tugadi!\n"
            f"To‘g‘ri javoblar: {score}/{total}\n"
            f"Foiz: {percent}%\n\n"
            f"{status}"
        )

        # Adminni ogohlantirish
        fullname = callback.from_user.full_name
        username = f"@{callback.from_user.username}" if callback.from_user.username else "yo‘q"
        await bot.send_message(
            ADMIN_ID,
            f"📊 {fullname} (ID: {user_id}, {username}) testni tugatdi.\n"
            f"✅ To‘g‘ri: {score}/{total}\n"
            f"📈 Foiz: {percent}%\n"
            f"{status}"
        )

        user_data.pop(user_id)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
