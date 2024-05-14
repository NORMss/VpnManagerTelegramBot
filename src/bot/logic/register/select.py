from decimal import Decimal

from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from src.api.payment import PaymentCase
from .router import register_router
from ...add_channel import add_channel
from ...structures.fsm.register import RegisterGroup, RegisterForBuyer, RegisterForSeller
from ...structures.keyboards.payment import get_payment_keyboard
from ...structures.keyboards.register import REGISTER_START_CONFIRM, REGISTER_RULES_READ
from ...structures.role import ProfileType


@register_router.message(F.text == "Начать регистрацию", RegisterGroup.confirmation)
async def register_confirmation(message: Message, state: FSMContext):
    await state.set_state(RegisterGroup.select)
    return (await message.answer(
        text="Выбери тип своего профиля",
        reply_markup=REGISTER_START_CONFIRM,
    )

            @ register_router.message(F.text == "Я хочу покупать рекламу", RegisterGroup.confirmation))


@register_router.message(F.text == "Я хочу покупать рекламу", RegisterGroup.confirmation)
async def register_confirmation(message: Message, state: FSMContext):
    await state.update_data({
        'role': ProfileType.SELLER,
    })
    await state.set_state(RegisterForBuyer.rules)
    await message.answer(
        text="Ознакомьтесь с правилами",
        reply_markup=REGISTER_RULES_READ,
    )


@register_router.message(F.text == "Я владелец канала(ов) и хочу продавать рекламу", RegisterGroup.confirmation)
async def register_confirmation(message: Message, state: FSMContext):
    await state.update_data({
        'role': ProfileType.SELLER,
    })
    await state.set_state(RegisterForBuyer.rules)
    await message.answer(
        text="Ознакомьтесь с правилами",
        reply_markup=REGISTER_RULES_READ,
    )


@register_router.callback_query(F.data == "read_rules", RegisterForSeller.rules)
async def read_rules(call: CallbackQuery, state: FSMContext):
    await state.set_state(RegisterForSeller.add_tg_channel)
    return await call.message.answer('Для продолжение регистрации необходимо добавить хотя бы один телеграм канал.'
                                     'Отправь ссылку на свой канал для дальнейшей регистрации.\n'
                                     'Канал будет проверяться модераторами.')


@register_router.message(RegisterForSeller.add_tg_channel)
async def add_tg_chanel(message: Message, state: FSMContext):
    await state.clear()
    await add_channel(message.from_user, message.text)
    return await message.answer('Твой канал отправлен на проверку')


@register_router.callback_query(F.data == "read_rules", RegisterForBuyer.rules)
async def read_rules(call: CallbackQuery, state: FSMContext):
    await state.set_state(RegisterForBuyer.fund)
    p_case = PaymentCase(user_id=call.from_user.id, value=Decimal(5))
    await call.message.answer('Для продолжения регистрации необходимо пополнить аккаунт ну сумму от 5$',
                              reply_markup=get_payment_keyboard(p_case)
                              )
