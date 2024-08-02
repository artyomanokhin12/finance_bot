from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.inline_keyboards.incomes_spendings_keyboard import incomes_buttons

router = Router()


@router.message(Command(commands=['income']))
async def incomes_command(message: Message):
    await message.answer(
        'Пожалуйста, выберите тип дохода',
        reply_markup = await incomes_buttons()
    )
    