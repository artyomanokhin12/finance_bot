""" Модуль для управления расходами """

from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message
from sqlalchemy.exc import CompileError, IntegrityError

from app.inline_keyboards.incomes_spendings_keyboard import spendings_buttons
from app.lexicon import LEXICON
from app.spendings_bank.dao import SpendingsBankDAO
from app.state import FSMSpendings
from app.users.dao import UsersDAO

router = Router()


@router.message(Command(commands=["spending"]), StateFilter(default_state))
async def spendings_command(message: Message, state: FSMContext):
    """Функция для вывода всех категорий расходов"""

    if not await UsersDAO.find_by_id(message.from_user.id):
        return await message.answer(LEXICON["reset"])

    await message.answer(
        LEXICON["spending_start"], reply_markup=await spendings_buttons()
    )
    await state.set_state(FSMSpendings.spending_fk)


@router.message(Command(commands=["spendings"]), ~StateFilter(default_state))
async def spendings_command_in_state(message: Message):
    """Функция для вывода всех категорий расходов в активном состоянии"""
    await message.answer(LEXICON["cancel"])


@router.message(StateFilter(FSMSpendings.spending_fk))
async def user_income_wrong_category(message: Message):
    """Функция-обработчик ошибки выбора пользователем категории"""
    await message.answer(LEXICON["wrong_category"])


@router.callback_query(StateFilter(FSMSpendings.spending_fk))
async def user_income_category(callback: CallbackQuery, state: FSMContext) -> None:
    """Функция выбора пользователем категории и переход на ввод суммы денег"""
    await state.update_data(spending_fk=int(callback.data))
    await callback.message.answer("Введите, пожалуйста, сумму расхода:")
    await callback.answer()
    await state.set_state(FSMSpendings.amount)


@router.message(StateFilter(FSMSpendings.amount))
async def user_new_income(message: Message, state: FSMContext):
    """Функция добавления количества денег пользователем"""
    try:
        if message.text.startswith("-"):
            return await message.answer(LEXICON["minus"])
        if message.text.count(",") > 0:
            user_answer = float(message.text.replace(",", ".", 1))
        else:
            user_answer = float(message.text)
        if len(message.text) > 8:
            return await message.answer(
                LEXICON["big_int"]
            )
        await state.update_data(amount=float(user_answer))
        data = await state.get_data()
        data["amount"] = round(data["amount"], 2)
        result = await SpendingsBankDAO.add(user_fk=message.from_user.id, **data)
        await message.answer(result)
        await state.clear()
    except ValueError:
        return await message.answer(LEXICON["error_wrong_value"])
    except IntegrityError:
        return await message.answer(LEXICON["error_server"])
    except CompileError:
        return await message.answer(LEXICON["error_server"])
    except UnboundLocalError:
        return await message.answer(LEXICON["error_server"])
