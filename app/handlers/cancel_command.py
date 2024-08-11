""" модуль для выхода состояния """

from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.lexicon import LEXICON


router = Router()


@router.message(Command(commands=['cancel']), StateFilter(default_state))
async def cancel_command_without_state(message: Message):
    """ Функция для выхода из состояния при неактивном состоянии """
    return await message.answer(
        LEXICON['cancel_without_state']
    )


@router.message(Command(commands=['cancel']), ~StateFilter(default_state))
async def cancel_command(message: Message, state: FSMContext):
    """ Функция для выхода из состояния при активном состоянии """
    await state.clear()
    return await message.answer(
        LEXICON['cancel_with_state']
    )

