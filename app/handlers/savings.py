from re import L
from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.exc import IntegrityError, CompileError

from app.lexicon import LEXICON
from app.state import FSMSaving, FSMSavingAction, FSMSavingDelete
from app.saving.dao import UsersSavingDAO
from app.inline_keyboards.incomes_spendings_keyboard import savings_buttons

router = Router()


@router.message(Command(commands=["saving"]), StateFilter(default_state))
async def saving_message(message: Message, state: FSMContext):
    await state.set_state(FSMSaving.goal_name)
    return await message.answer("Пожалуйста, укажите наименование цели, на которую вы собираетесь откладывать")


@router.message(Command(commands=["saving"]), ~StateFilter(default_state))
async def saving_command_in_state(message: Message):
    return await message.answer("Вы уже находитесь в состоянии")


@router.message(StateFilter(FSMSaving.goal_name))
async def set_goal_name(message: Message, state: FSMContext):
    await state.update_data(goal_name=message.text)
    await state.set_state(FSMSaving.amount)
    return await message.answer("Пожалуйста, введите сумму, которую планируете накопить")


@router.message(StateFilter(FSMSaving.amount))
async def set_amount(message: Message, state: FSMContext):
    if not message.text.isdecimal():
        return await message.answer(LEXICON["limit_wrong"])
    elif len(message.text) > 8:
        return await message.answer(LEXICON["big_int"])
    elif message.text.startswith("-"):
        return await message.answer(LEXICON["minus"])
    
    try:
        data = await state.get_data()
        await UsersSavingDAO.add(
            user_id=message.from_user.id, 
            amount=int(message.text),
            current_savings=0, 
            **data
            )
        await state.clear()
        return await message.answer("Строка сбережения добавлена")
    except ValueError:
        return await message.answer(LEXICON["error_wrong_value"])
    except IntegrityError:
        return await message.answer(LEXICON["error_server"])
    except CompileError:
        return await message.answer(LEXICON["error_server"])
    

@router.message(Command(commands="show_savings"))
async def show_all_savings(message: Message):
    goals = await UsersSavingDAO.find_all_by_filter(user_id=message.from_user.id)
    ans = ""
    if not goals:
        return await message.answer("На данный момент целей для накопления нет")
    for goal in goals:
        ans = ans + str(goal) + "\n"
    return await message.answer(ans)
    

@router.message(Command(commands="delete_goal"), StateFilter(default_state))
async def choose_goal_for_delete(message: Message, state: FSMContext):
    await state.set_state(FSMSavingDelete.choose_goal)
    return await message.answer(
        text="Пожалуйста, выберите цель, которую хотите удалить:",
        reply_markup=await savings_buttons(id=message.from_user.id),
    )


@router.message(Command(commands="delete_goal"), ~StateFilter(default_state))
async def choose_goal_for_delete_in_state(message: Message):
    return await message.answer("Вы уже находитесь в состоянии выбора")


@router.message(StateFilter(FSMSavingDelete.choose_goal))
async def wrong_choose_goal(message: Message):
    return await message.answer("Пожалуйста, выберите цель среди доступных")


@router.callback_query(StateFilter(FSMSavingDelete.choose_goal))
async def delete_goal(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.answer()
        result = await UsersSavingDAO.delete_saving(
            user_id=callback.from_user.id, 
            goal_name=callback.data,
            )
        await state.clear()
        return await callback.message.answer(result)
    except Exception:
        return await callback.message.answer("Что-то пошло не так")    


@router.message(Command(commands="add_saving_money"), StateFilter(default_state))
async def add_saving_money_command(message: Message, state: FSMContext):
    await state.set_state(FSMSavingAction.choose_goal)
    return await message.answer(
        text="Выберите, пожалуйста, цель, куда хотите внести сумму:",
        reply_markup=await savings_buttons(id=message.from_user.id),
    )


@router.message(Command(commands="add_saving_money"), ~StateFilter(default_state))
async def add_saving_money_command_in_state(mesasge: Message):
    return await mesasge.answer("Вы уже находитесь в состоянии")


@router.callback_query(StateFilter(FSMSavingAction.choose_goal))
async def input_money(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(choose_goal=callback.data)
    await state.set_state(FSMSavingAction.input_money)
    return await callback.message.answer("Введите, пожалуйста, целочисленную сумму, которую хотите отложить для данной цели:")

@router.message(StateFilter(FSMSavingAction.choose_goal))
async def wrong_choose_goal_name(message: Message):
    return await message.answer("Пожалуйста, выберите цель из списка")

@router.message(StateFilter(FSMSavingAction.input_money))
async def final_input_money_for_goal(message: Message, state: FSMContext):
    if not message.text.isdecimal():
        return await message.answer(LEXICON["limit_wrong"])
    elif len(message.text) > 8:
        return await message.answer(LEXICON["big_int"])
    elif message.text.startswith("-") or message.text.startswith("0"):
        return await message.answer(LEXICON["minus"])
    
    try:
        data = await state.get_data()
        deposit = message.text
        result = await UsersSavingDAO.update_goal(
            user_id=message.from_user.id,
            goal_name=data["choose_goal"],
            current_deposit=int(deposit),
        )
        await state.clear()
        return await message.answer(result)
    except Exception as e:
        print(e)
        return await message.answer("Произошла ошибка")
