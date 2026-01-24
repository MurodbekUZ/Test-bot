from aiogram import types, Router
from aiogram.filters import CommandStart
from keyboards.inline.quiz import grades_keyboard
from states.quiz import QuizState
from aiogram.fsm.context import FSMContext

router = Router()

@router.message(CommandStart())
async def bot_start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        f"👋 Salom, {message.from_user.full_name}!\n\n"
        "Men Matematika Test Botiman.\n"
        "Testni boshlash uchun sinfni tanlang:",
        reply_markup=grades_keyboard()
    )
    await state.set_state(QuizState.select_grade)
