""" Модуль начала пользования ботом и добавления лимита трат """

from aiogram import Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.state import FSMInputLimit
from app.users.dao import UsersDAO


router = Router()


@router.message(CommandStart())
async def start_command(message: Message):
    """ Функция старта пользования ботом """
    status = await UsersDAO.find_by_id(message.from_user.id)

    if status:
        await message.answer(
            'С возвращением! На данный момент у тебя остался тот же баланс, что и при последнем использовании.\n'
            'Если хочешь начать все с начала, то подожди.'
        )
    else:
        print(message.from_user.id)
        await UsersDAO.add(id=message.from_user.id)
        
        await message.answer(
            'Привет! Добро пожаловать в финансового бота. Здесь вы можете отслеживать считать свои финансы.\n'
            'По желанию, вы можете добавить себе ограничение в бюджете, чтобы отслеживать, сколько вы потратили за месяц.\n'
            'Для получения более подробной информации о лимите, вы можете обратиться к команде /help'
        )

@router.message(CommandStart(), ~StateFilter(default_state))
async def start_command_in_state(message: Message):
    """ Функция-обработчик команды старта в режиме состояния """
    await message.answer(
        'Вы уже находитесь в состоянии выбора (from start)'
    )


@router.message(Command(commands=['limit']), StateFilter(default_state))
async def input_limit(message: Message, state: FSMContext):
    """ Функция начала добавления лимита """
    await message.answer(
        'Пожалуйста, введите лимит трат на месяц.\n'
        'Формат ввода: целочисленный <123, 1000, 5555>'
    )

    await state.set_state(FSMInputLimit.limit)


@router.message(Command(commands=['limit']), ~StateFilter(default_state))
async def input_limit_in_state(message: Message):
    """ Функция-обработчик команды лимита в режиме состояния """
    await message.answer(
        'Вы уже находитесь в состоянии ввода инфомации (из модуля limit).\n' 
        'Если вы хотите прервать выполнение операции, пожалуйста, введите /cancel.\n'
    )


@router.message(StateFilter(FSMInputLimit.limit))
async def final_input_limit(message: Message, state: FSMContext):
    """ Функция внесения пользователем лимита и внесение информации в базу данных """

    if not message.text.isdecimal():
        return await message.answer(
            'Неправильный формат ввода данных. Пожалуйста, еще раз введите ваш лимит в соответствии с форматом.\n'
            'Формат ввода: целочисленный <123, 1000, 5555 и тому подобное>'
        )

    await state.update_data(limit=message.text)
    data = await state.get_data()
    await UsersDAO.update_by_id(
        id=message.from_user.id,
        users_limit=data['limit'],
    )
    await state.clear()
    await message.answer(
        'Вы успешно добавили свой месячный лимит!'
    )
