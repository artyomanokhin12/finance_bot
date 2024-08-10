from datetime import date, timedelta

from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from app.state import FSMState

from app.stat_request import get_stats
from app.inline_keyboards.incomes_spendings_keyboard import period_buttons

router = Router()


@router.message(Command(commands=['stat']), StateFilter(default_state))
async def stat_command(message: Message, state: FSMContext):
    await state.set_state(FSMState.period)
    return await message.answer(
        'Пожалуйста, выберите период для отображения статистики',
        reply_markup = await period_buttons()
    )

@router.message(Command(commands=['stat']), ~StateFilter(default_state))
async def stat_command_with_state(message: Message):
    return await message.answer(
        'Вы уже находитесь в состоянии выбора'
    )

@router.message(StateFilter(FSMState.period))
async def user_income_wrong_category(message: Message):
    ''' Функция-обработчик ошибки выбора пользователем категории '''
    await message.answer(
        'Ошибка выбора периода. Пожалуйста, выберите период из доступного перечня.'
    )

@router.callback_query(StateFilter(FSMState.period))
async def stat_test_command(callback: CallbackQuery, state: FSMContext):
    """ Функция для отображения статистики пользователя """
    await callback.answer()
    await callback.message.delete()

    period = callback.data
    
    match period:
        case 'day':
            date_from = date.today()
            date_to = date_from + timedelta(days=1)
            print('date_from=', date_from, 'date_to=', date_to)
        case 'week':
            date_to = date.today() + timedelta(days=1)
            date_from = date_to - timedelta(days=7)
            print('date_from=', date_from, 'date_to=', date_to)
        case 'month':
            date_to = date.today().replace(day=1)
            date_from = (date_to - timedelta(days=date_to.day)).replace(day=1)
            print('date_from=', date_from, 'date_to=', date_to)

    result = await get_stats(
        user_id = callback.from_user.id, 
        date_from = date_from,
        date_to = date_to,
        ) 
    await state.clear()
    return await callback.message.answer(
        result
    )
    