from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.spendings.dao import SpendingsDAO
from app.spendings.models import Spendings
from app.incomes.dao import IncomesDAO
from app.incomes.models import Incomes

async def spendings_buttons() -> InlineKeyboardMarkup:
    """ Функция создания инлайн-кнопок расходов """
    buttons = []
    categories: list[Spendings] = await SpendingsDAO.find_all()
    kb_builder = InlineKeyboardBuilder()
    for category in categories:
        buttons.append(
            InlineKeyboardButton(
                text=category.ru_spending_name,
                callback_data=category.spendings_name,
            )
        )
    kb_builder.row(*buttons, width=3)
    return kb_builder.as_markup()


async def incomes_buttons() -> InlineKeyboardMarkup:
    """ Функция создания инлайн-кнопок расходов """
    buttons = []
    categories: list[Incomes] = await IncomesDAO.find_all()
    kb_builder = InlineKeyboardBuilder()
    for category in categories:
        buttons.append(
            InlineKeyboardButton(
                text=category.ru_incomes_name,
                callback_data=category.incomes_name,
            )
        )
    kb_builder.row(*buttons, width=3)
    return kb_builder.as_markup()