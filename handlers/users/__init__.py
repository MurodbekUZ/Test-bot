from aiogram import Router
from . import start, help, quiz

router = Router()

router.include_router(start.router)
router.include_router(help.router)
router.include_router(quiz.router)
