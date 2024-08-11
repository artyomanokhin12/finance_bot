from aiogram import Router
from aiogram.types import Message

from app.lexicon import LEXICON

router = Router()


@router.message()
async def empty_message(message: Message):
    return await message.answer(
        LEXICON['unknown_message']
    )
