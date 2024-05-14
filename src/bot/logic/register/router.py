from aiogram import Router

from src.bot.filters.register_filter import RegisterFilter
from src.bot.structures.fsm.register import RegisterGroup

register_router = Router(name='Register')
register_router.message.filter(RegisterGroup)
register_router.message.filter(RegisterFilter())