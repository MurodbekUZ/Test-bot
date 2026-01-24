from aiogram import types, Router
from aiogram.filters import Command

router = Router()

@router.message(Command("help"))
async def bot_help(message: types.Message):
    await message.answer(
        "🆘 <b>Yordam</b>\n\n"
        "Botdan foydalanish uchun /start tugmasini bosing va sinfni tanlang.\n"
        "Har bir testda 30 ta savol mavjud.\n"
        "Javob berishga shoshilmang, vaqt chegaralanmagan."
    )
