""" Модуль начала пользования ботом и добавления лимита трат """

from aiogram import Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.state import FSMInputLimit
from app.users.dao import UsersDAO
from app.lexicon import LEXICON


router = Router()


@router.message(CommandStart())
async def start_command(message: Message):
    """ Функция старта пользования ботом """
    status = await UsersDAO.find_by_id(message.from_user.id)

    if status:
        await message.answer(
            LEXICON['return']
        )
    else:
        print(message.from_user.id)
        await UsersDAO.add(id=message.from_user.id)
        
        await message.answer(
            LEXICON['start']
        )

@router.message(CommandStart(), ~StateFilter(default_state))
async def start_command_in_state(message: Message):
    """ Функция-обработчик команды старта в режиме состояния """
    await message.answer(
        LEXICON['cancel']
    )


@router.message(Command(commands=['limit']), StateFilter(default_state))
async def input_limit(message: Message, state: FSMContext):
    """ Функция начала добавления лимита """
    await message.answer(
        LEXICON['limit_start']
    )

    await state.set_state(FSMInputLimit.limit)


@router.message(Command(commands=['limit']), ~StateFilter(default_state))
async def input_limit_in_state(message: Message):
    """ Функция-обработчик команды лимита в режиме состояния """
    await message.answer(
        LEXICON['cancel']
    )


@router.message(StateFilter(FSMInputLimit.limit))
async def final_input_limit(message: Message, state: FSMContext):
    """ Функция внесения пользователем лимита и внесение информации в базу данных """

    if not message.text.isdecimal():
        return await message.answer(
            LEXICON['limit_wrong']
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
