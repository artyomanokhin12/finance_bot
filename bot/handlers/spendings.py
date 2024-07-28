from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command(commands=['spending']))
async def spending_command(message: Message):
    await message.answer(
        'Пожалуйста, выберите тип расхода'
    )
    