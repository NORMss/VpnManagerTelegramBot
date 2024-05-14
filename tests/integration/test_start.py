from aiogram import Dispatcher

from src.bot.structures.keyboards.register import REGISTER_START_CONFIRM
from tests.utils.mocked_bot import MockedBot

from aiogram.methods import SendMessage

import pytest

from tests.utils.updates import get_update, get_message


@pytest.mark.asyncio
async def test_start(bot: MockedBot, dp: Dispatcher):
    start_command = get_update(get_message('/start'))
    result = await dp.feed_update(bot, start_command)
    assert isinstance(result, SendMessage)
    assert result.text == 'Привет!'
    assert result.reply_markup == REGISTER_START_CONFIRM
