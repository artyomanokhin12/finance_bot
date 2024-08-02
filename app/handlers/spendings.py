from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.inline_keyboards.incomes_spendings_keyboard import spendings_buttons

router = Router()


@router.message(Command(commands=['spending']))
async def spending_command(message: Message):
    await message.answer(
        'Пожалуйста, выберите тип расхода',
        reply_markup = await spendings_buttons()
    )
    