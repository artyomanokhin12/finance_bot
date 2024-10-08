from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.incomes.dao import IncomesDAO
from app.incomes.models import Incomes
from app.saving.models import UsersSaving
from app.spendings.dao import SpendingsDAO
from app.spendings.models import Spendings
from app.saving.dao import UsersSavingDAO


async def get_all_incomes() -> list[Incomes]:
    return await IncomesDAO.find_all()


async def get_all_spendings() -> list[Spendings]:
    return await SpendingsDAO.find_all()

async def get_all_savings(id: int) -> list[UsersSaving]:
    return await UsersSavingDAO.find_all_by_filter(user_id=id)


async def spendings_buttons() -> InlineKeyboardMarkup:
    """Функция создания инлайн-кнопок расходов"""
    buttons = []
    categories: list[Spendings] = await get_all_spendings()
    kb_builder = InlineKeyboardBuilder()
    for category in categories:
        buttons.append(
            InlineKeyboardButton(
                text=category.spending_name,
                callback_data=str(category.id),
            )
        )
    kb_builder.row(*buttons, width=3)
    return kb_builder.as_markup()


async def incomes_buttons() -> InlineKeyboardMarkup:
    """Функция создания инлайн-кнопок доходов"""
    buttons = []
    categories: list[Incomes] = await get_all_incomes()
    kb_builder = InlineKeyboardBuilder()
    for category in categories:
        buttons.append(
            InlineKeyboardButton(
                text=category.incomes_name,
                callback_data=str(category.id),
            )
        )
    kb_builder.row(*buttons, width=3)
    return kb_builder.as_markup()


async def period_buttons() -> InlineKeyboardMarkup:

    period = {
        "day": "День",
        "week": "Неделя",
        "curr_month": "Текущий месяц",
        "prev_month": "Прошлый месяц",
    }
    buttons = []
    kb_builder = InlineKeyboardBuilder()
    for key, value in period.items():
        buttons.append(
            InlineKeyboardButton(
                text=value,
                callback_data=key,
            )
        )
    kb_builder.row(*buttons, width=2)
    return kb_builder.as_markup()


async def reset_keyboard() -> InlineKeyboardMarkup:

    buttons = {
        "yes": "Да",
        "no": "Нет",
    }

    button = []
    kb_builder = InlineKeyboardBuilder()
    for key, value in buttons.items():
        button.append(InlineKeyboardButton(text=value, callback_data=key))
    kb_builder.row(*button, width=2)
    return kb_builder.as_markup()

async def savings_buttons(id: int) -> InlineKeyboardMarkup:
    button = []
    user_savings: list[UsersSaving] = await get_all_savings(id)
    kb_builder = InlineKeyboardBuilder()
    for goal in user_savings:
        button.append(InlineKeyboardButton(text=goal.goal_name, callback_data=goal.goal_name))
    kb_builder.row(*button, width=1)
    return kb_builder.as_markup()
