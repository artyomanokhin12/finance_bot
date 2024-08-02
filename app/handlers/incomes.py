""" Модуль для управления доходами """

from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.incomes_bank.dao import IncomesBankDAO
from app.inline_keyboards.incomes_spendings_keyboard import incomes_buttons
from app.state import FSMIncomes

router = Router()

@router.message(Command(commands=['income']), StateFilter(default_state))
async def incomes_command(message: Message, state: FSMContext):
    """ Функция для вывода всех категорий доходов """
    await message.answer(
        'Пожалуйста, выберите тип дохода',
        reply_markup = await incomes_buttons()
    )
    await state.set_state(FSMIncomes.incomes_fk)


@router.message(Command(commands=['income']), ~StateFilter(default_state))
async def incomes_command(message: Message):
    """ Функция для вывода всех категорий доходов в активном состоянии """
    await message.answer(
        'Вы уже находитесь в состоянии выбора.\n'
        'Если хотите отменить операцию, пожалуйста, выберите команду '
        '/cancel в меню бота.',
    )
    

@router.message(StateFilter(FSMIncomes.incomes_fk))
async def user_income_wrong_category(message: Message):
    ''' Функция-обработчик ошибки выбора пользователем категории '''
    await message.answer(
        'Ошибка выбора категории. Пожалуйста, выберите категорию из списка.'
    )

@router.callback_query(StateFilter(FSMIncomes.incomes_fk))
async def user_income_category(callback: CallbackQuery, state: FSMContext) -> None:
    ''' Функция выбора пользователем категории и переход на ввод суммы денег '''
    await state.update_data(incomes_fk=int(callback.data))
    await callback.message.answer(
        'Введите, пожалуйста, сумму пополнения:'
    )
    await state.set_state(FSMIncomes.amount)

@router.message(StateFilter(FSMIncomes.amount))
async def user_new_income(message: Message, state: FSMContext):
    ''' Функция добавления количества денег пользователем '''
    user_answer = message.text
    ''' Тут корявая проверка на float. Переделать '''
    # if user_answer.count(',') > 0:
    #     user_answer.replace(',','.', 1)
    
    if not isinstance(float(user_answer), float):
        return await message.answer(
            'Ошибка: некорректное значение. Пожалуйста, введите целочисленное число или число с запятой'
        )

    try:
        await state.update_data(amount=float(user_answer))
        data = await state.get_data()
        await IncomesBankDAO.add(user_fk=message.from_user.id, **data)
        await message.answer(
            'Строка дохода успешно добавлена!'
        )
        await state.clear()
    except Exception:
        return await message.answer(
            'Во время добавления дохода возникла ошибка. Пожалуйста, повторите процесс'
        )
