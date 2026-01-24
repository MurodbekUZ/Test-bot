from loader import dp
from . import users

dp.include_router(users.router)
