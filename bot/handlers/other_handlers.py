from aiogram import Router
from aiogram.types import Message

router = Router()


@router.message()
async def empty_message(message: Message):
    return await message.answer(
        'Я не поддерживаю данную команду или сообщение. Пожалуйста, выберите те команды, которые представлены в меню.'
    )
