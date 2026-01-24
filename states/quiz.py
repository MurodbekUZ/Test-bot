from aiogram.fsm.state import StatesGroup, State

class QuizState(StatesGroup):
    select_grade = State()
    solving = State()
