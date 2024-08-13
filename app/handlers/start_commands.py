""" Модуль начала пользования ботом и добавления лимита трат """

from aiogram import Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message

from app.inline_keyboards.incomes_spendings_keyboard import reset_keyboard
from app.lexicon import LEXICON
from app.state import FSMInputLimit, FSMReset
from app.users.dao import UsersDAO

router = Router()


@router.message(CommandStart())
async def start_command(message: Message):
    """Функция старта пользования ботом"""

    if await UsersDAO.find_by_id(message.from_user.id):
        return await message.answer(LEXICON["return"])
    else:
        await UsersDAO.add(id=message.from_user.id, current_balance=0)
        return await message.answer(LEXICON["start"])


@router.message(CommandStart(), ~StateFilter(default_state))
async def start_command_in_state(message: Message):
    """Функция-обработчик команды старта в режиме состояния"""
    await message.answer(LEXICON["cancel"])


@router.message(Command(commands=["limit"]), StateFilter(default_state))
async def input_limit(message: Message, state: FSMContext):
    """Функция начала добавления лимита"""
    await message.answer(LEXICON["limit_start"])

    await state.set_state(FSMInputLimit.limit)


@router.message(Command(commands=["limit"]), ~StateFilter(default_state))
async def input_limit_in_state(message: Message):
    """Функция-обработчик команды лимита в режиме состояния"""
    await message.answer(LEXICON["cancel"])


@router.message(StateFilter(FSMInputLimit.limit))
async def final_input_limit(message: Message, state: FSMContext):
    """Функция внесения пользователем лимита и внесение информации в базу данных"""

    if not message.text.isdecimal():
        return await message.answer(LEXICON["limit_wrong"])
    elif len(message.text) > 8:
        return await message.answer(
                LEXICON["big_int"]
        )
    elif message.text.startswith("-"):
        return await message.answer(
            LEXICON["minus"]
        )
    await state.update_data(limit=message.text)
    data = await state.get_data()
    await UsersDAO.update_by_id(
        id=message.from_user.id,
        users_limit=data["limit"],
    )
    await state.clear()
    await message.answer("Вы успешно добавили свой месячный лимит!")


@router.message(Command(commands=["reset"]), StateFilter(default_state))
async def reset_func(message: Message, state: FSMContext):
    await message.answer(
        LEXICON["reset_info"],
        reply_markup=await reset_keyboard(),
    )
    await state.set_state(FSMReset.confirmation)


@router.message(Command(commands=["reset"]), ~StateFilter(default_state))
async def reset_command_in_state(message: Message):
    return await message.answer(LEXICON["cancel"])


@router.message(StateFilter(FSMReset.confirmation))
async def wrong_reset_in_state(message: Message):
    return await message.answer("Пожалуйста, нажмите на одну из предложенных кнопок.")


@router.callback_query(StateFilter(FSMReset.confirmation))
async def main_reset(callback: CallbackQuery, state: FSMContext):
    if callback.data == "no":
        await state.clear()
        await callback.answer()
        return await callback.message.answer("Отмена операции")
    elif callback.data == "yes":
        await UsersDAO.delete(user_id=callback.from_user.id)
        await state.clear()
        await callback.answer()
        return await callback.message.answer(
            "Все записи с вашими доходами и расходами удалены. Чтобы начать пользоваться ботом снвоа, пожалуйста, введите команду /start"
        )
