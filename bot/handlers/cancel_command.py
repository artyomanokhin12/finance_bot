from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.types import Message


router = Router()


@router.message(Command(commands=['cancel']), StateFilter(default_state))
async def cancel_command_without_state(message: Message):
    return await message.answer(
        'Вы не находитесь в состоянии выполнения функции или команды. Отмена не нужна'
    )


@router.message(Command(commands=['cancel']), ~StateFilter(default_state))
async def cancel_command(message: Message, state: FSMContext):
    await state.clear()
    return await message.answer(
        'Вы вышли из состояния выполнения функции!'
    )

