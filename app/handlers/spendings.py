""" Модуль для управления расходами """

from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.exc import IntegrityError, CompileError

from app.inline_keyboards.incomes_spendings_keyboard import spendings_buttons
from app.spendings_bank.dao import SpendingsBankDAO
from app.state import FSMSpendings

router = Router()

@router.message(Command(commands=['spending']), StateFilter(default_state))
async def incomes_command(message: Message, state: FSMContext):
    """ Функция для вывода всех категорий расходов """
    await message.answer(
        'Пожалуйста, выберите тип расхода',
        reply_markup = await spendings_buttons()
    )
    await state.set_state(FSMSpendings.spending_fk)


@router.message(Command(commands=['spendings']), ~StateFilter(default_state))
async def incomes_command(message: Message):
    """ Функция для вывода всех категорий расходов в активном состоянии """
    await message.answer(
        'Вы уже находитесь в состоянии выбора (from spending).\n'
        'Если хотите отменить операцию, пожалуйста, выберите команду '
        '/cancel в меню бота.',
    )
    

@router.message(StateFilter(FSMSpendings.spending_fk))
async def user_income_wrong_category(message: Message):
    ''' Функция-обработчик ошибки выбора пользователем категории '''
    await message.answer(
        'Ошибка выбора категории. Пожалуйста, выберите категорию из списка.'
    )

@router.callback_query(StateFilter(FSMSpendings.spending_fk))
async def user_income_category(callback: CallbackQuery, state: FSMContext) -> None:
    ''' Функция выбора пользователем категории и переход на ввод суммы денег '''
    await state.update_data(spending_fk=int(callback.data))
    await callback.message.answer(
        'Введите, пожалуйста, сумму пополнения:'
    )
    await callback.answer()
    await state.set_state(FSMSpendings.amount)

@router.message(StateFilter(FSMSpendings.amount))
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
        await SpendingsBankDAO.add(user_fk=message.from_user.id, **data)
        await message.answer(
            'Строка расхода успешно добавлена!'
        )
        await state.clear()
    except ValueError:
        return await message.answer(
            'Ошибка: некорректное значение. Пожалуйста, введите целочисленное число или число с запятой'
        )
    except IntegrityError as i:
        print(i)
        return await message.answer(
            'Проихошла ошибка. Пожалуйста, повторите операцию с момента ввода суммы'
        )
    except CompileError as e:
        print(e)
        return await message.answer(
            'Проихошла ошибка. Пожалуйста, повторите операцию с момента ввода суммы'
        )
    except UnboundLocalError as e:
        print(e)
        return await message.answer(
            'Проихошла ошибка. Пожалуйста, повторите операцию с момента ввода суммы'
        )