""" Модуль для управления доходами """

from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.exc import IntegrityError, CompileError

from app.incomes_bank.dao import IncomesBankDAO
from app.inline_keyboards.incomes_spendings_keyboard import incomes_buttons
from app.state import FSMIncomes
from app.lexicon import LEXICON

router = Router()

@router.message(Command(commands=['income']), StateFilter(default_state))
async def incomes_command(message: Message, state: FSMContext):
    """ Функция для вывода всех категорий доходов """
    await message.answer(
        LEXICON['incomes_start'],
        reply_markup = await incomes_buttons()
    )
    await state.set_state(FSMIncomes.incomes_fk)

@router.message(Command(commands=['income']), ~StateFilter(default_state))
async def incomes_command(message: Message):
    """ Функция для вывода всех категорий доходов в активном состоянии """
    await message.answer(
        LEXICON['cancel'],
    )
    
@router.message(StateFilter(FSMIncomes.incomes_fk))
async def user_income_wrong_category(message: Message):
    ''' Функция-обработчик ошибки выбора пользователем категории '''
    await message.answer(
        LEXICON['wrong_category']
    )

@router.callback_query(StateFilter(FSMIncomes.incomes_fk))
async def user_income_category(callback: CallbackQuery, state: FSMContext) -> None:
    ''' Функция выбора пользователем категории и переход на ввод суммы денег '''
    await state.update_data(incomes_fk=int(callback.data))
    await callback.answer()
    await callback.message.answer(
        'Введите, пожалуйста, сумму пополнения:'
    )
    await state.set_state(FSMIncomes.amount)

@router.message(StateFilter(FSMIncomes.amount))
async def user_new_income(message: Message, state: FSMContext):
    ''' Функция добавления количества денег пользователем '''
    try:
        if message.text.count(',') > 0:
            user_answer = float(message.text.replace(',','.', 1))
        else:
            user_answer = float(message.text)
            
        await state.update_data(amount=float(user_answer))
        data = await state.get_data()
        data['amount'] = round(data['amount'], 2)
        result = await IncomesBankDAO.add(user_fk=message.from_user.id, **data)
        await message.answer(
            result
        )
        await state.clear()
    except ValueError:
        return await message.answer(
            LEXICON['error_wrong_value']
        )
    except IntegrityError as i:
        return await message.answer(
            LEXICON['error_server']
        )
    except CompileError as e:
        return await message.answer(
            LEXICON['error_server']
        )
