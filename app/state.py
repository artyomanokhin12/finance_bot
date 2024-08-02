from aiogram.fsm.state import State, StatesGroup


class FSMInputLimit(StatesGroup):

    limit = State()


class FSMIncomes(StatesGroup):

    incomes_fk = State()
    amount = State()


class FSMSpendings(StatesGroup):

    spending_fk = State()
    amount = State()
