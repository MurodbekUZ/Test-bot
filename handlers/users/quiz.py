from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from states.quiz import QuizState
from utils.questions import generate_questions
from keyboards.inline.quiz import answers_keyboard, grades_keyboard

router = Router()

@router.callback_query(QuizState.select_grade, F.data.startswith("grade:"))
async def start_quiz(call: types.CallbackQuery, state: FSMContext):
    grade = int(call.data.split(":")[1])
    questions = generate_questions(grade=grade, num=30)
    
    # Save state
    await state.update_data(
        questions=questions,
        current_index=0,
        score=0,
        grade=grade
    )
    
    # Show first question
    q = questions[0]
    await call.message.edit_text(
        f"📘 <b>{grade}-sinf Testi</b>\n\n"
        f"Savol 1/30:\n"
        f"<b>{q['q']}</b>",
        reply_markup=answers_keyboard(0, q["options"])
    )
    await state.set_state(QuizState.solving)

@router.callback_query(QuizState.solving, F.data.startswith("ans:"))
async def check_answer(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_index = int(call.data.split(":")[1])
    ans_index = int(call.data.split(":")[2])
    
    questions = data.get("questions")
    current_q = questions[current_index]
    
    correct_index = current_q["answer"]
    is_correct = (ans_index == correct_index)
    
    # Update score
    if is_correct:
        await state.update_data(score=data["score"] + 1)
        await call.answer("✅ To'g'ri!")
    else:
        correct_text = current_q["options"][correct_index]
        await call.answer(f"❌ Noto'g'ri! Javob: {correct_text}", show_alert=True)
    
    # Next question
    next_index = current_index + 1
    if next_index < len(questions):
        next_q = questions[next_index]
        await state.update_data(current_index=next_index)
        await call.message.edit_text(
            f"Savol {next_index + 1}/{len(questions)}:\n"
            f"<b>{next_q['q']}</b>",
            reply_markup=answers_keyboard(next_index, next_q["options"])
        )
    else:
        # Finish
        score = data["score"] + (1 if is_correct else 0) # Add last point if just validated
        # Actually logic above added to state, let's re-read or just trust increment
        # Wait, if is_correct, I updated state... but local variable 'score' is from old data.
        # Let's get fresh data
        fresh_data = await state.get_data() 
        final_score = fresh_data["score"]
        
        percent = (final_score / 30) * 100
        result_text = "✅ O'tdingiz!" if percent >= 80 else "❌ Yiqildingiz!"
        
        await call.message.edit_text(
            f"🏁 <b>Test Yakunlandi!</b>\n\n"
            f"To'g'ri javoblar: {final_score}/30\n"
            f"Natija: {percent:.1f}%\n"
            f"{result_text}\n\n"
            f"Qayta ishlash uchun /start ni bosing."
        )
        await state.clear()
