from datetime import date, timedelta

from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message

from app.inline_keyboards.incomes_spendings_keyboard import period_buttons
from app.lexicon import LEXICON
from app.stat_request import get_stats
from app.state import FSMState
from app.users.dao import UsersDAO

router = Router()


@router.message(Command(commands=["stat"]), StateFilter(default_state))
async def stat_command(message: Message, state: FSMContext):

    if not await UsersDAO.find_by_id(message.from_user.id):
        return await message.answer(LEXICON["reset"])

    await state.set_state(FSMState.period)
    return await message.answer(
        LEXICON["stat_start"], reply_markup=await period_buttons()
    )


@router.message(Command(commands=["stat"]), ~StateFilter(default_state))
async def stat_command_with_state(message: Message):
    return await message.answer(LEXICON["cancel"])


@router.message(StateFilter(FSMState.period))
async def user_income_wrong_category(message: Message):
    """Функция-обработчик ошибки выбора пользователем категории"""
    return await message.answer(LEXICON["stat_period_error"])


@router.callback_query(StateFilter(FSMState.period))
async def stat_test_command(callback: CallbackQuery, state: FSMContext):
    """Функция для отображения статистики пользователя"""
    await callback.answer()
    await callback.message.delete()

    period = callback.data

    match period:
        case "day":
            date_from = date.today()
            date_to = date_from + timedelta(days=1)
            prev_month = False
            ans = f"Вывод статистики за {date_from.strftime("%d.%m.%Y")}\n"
        case "week":
            date_to = date.today() + timedelta(days=1)
            date_from = date_to - timedelta(days=7)
            prev_month = False
            ans = f"Вывод статистики за {date_from.strftime("%d.%m.%Y")} - {(date_to - timedelta(days=1)).strftime("%d.%m.%Y")}\n"
        case "prev_month":
            date_to = date.today().replace(day=1)
            date_from = (date_to - timedelta(days=date_to.day)).replace(day=1)
            prev_month = True
            ans = f"Вывод статистики за {date_from.strftime("%d.%m.%Y")} - {(date_to - timedelta(days=1)).strftime("%d.%m.%Y")}\n"
        case "curr_month":
            date_from = date.today().replace(day=1)
            date_to = date.today() + timedelta(days=1)
            prev_month = False
            ans = f"Вывод статистики за {date_from.strftime("%d.%m.%Y")} - {(date_to - timedelta(days=1)).strftime("%d.%m.%Y")}\n"

    result = await get_stats(
        user_id=callback.from_user.id,
        date_from=date_from,
        date_to=date_to,
        prev_month=prev_month,
    )
    await state.clear()
    return await callback.message.answer(ans + result)
