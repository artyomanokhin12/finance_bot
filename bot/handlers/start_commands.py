from aiogram import Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.state import FSMInputLimit
from bot.users.dao import UsersDAO


router = Router()


@router.message(CommandStart())
async def start_command(message: Message):
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


@router.message(Command(commands=['limit']), StateFilter(default_state))
async def input_limit(message: Message, state: FSMContext):
    await message.answer(
        'Пожалуйста, введите лимит трат на месяц.\n'
        'Формат ввода: целочисленный <123, 1000, 5555>'
    )

    await state.set_state(FSMInputLimit.limit)


@router.message(Command(commands=['limit']), ~StateFilter(default_state))
async def input_limit_in_state(message: Message):
    await message.answer(
        'Вы уже находитесь в состоянии ввода инфомации.\n' 
        'Если вы хотите прервать выполнение операции, пожалуйста, введите /cancel.\n'
    )


@router.message(StateFilter(FSMInputLimit.limit))
async def final_input_limit(message: Message, state: FSMContext):

    if not message.text.isdecimal():
        return await message.answer(
            'Неправильный формат ввода данных. Пожалуйста, еще раз введите ваш лимит в соответствии с форматом.\n'
            'Формат ввода: целочисленный <123, 1000, 5555 и тому подобное>'
        )

    await state.update_data(limit=message.text)
    data = await state.get_data()
    print(data['limit'])
    await UsersDAO.update(
        id=message.from_user.id,
        limit=data['limit'],
    )
    await state.clear()