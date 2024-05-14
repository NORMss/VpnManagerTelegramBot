from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.api.payment import get_payment_url


def get_payment_keyboard(payment_case) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=f'Пополнить аккаунт на {payment_case.value}₽',
                url=get_payment_url(payment_case))]
        ]
    )
