from aiogram.fsm.state import State, StatesGroup


class FSMInputLimit(StatesGroup):

    limit = State()


class FSMIncomes(StatesGroup):

    incomes_fk = State()
    amount = State()


class FSMSpendings(StatesGroup):

    spending_fk = State()
    amount = State()


class FSMState(StatesGroup):

    period = State()


class FSMReset(StatesGroup):

    confirmation = State()


class FSMSaving(StatesGroup):

    goal_name = State()
    amount = State()


class FSMSavingDelete(StatesGroup):

    choose_goal = State()


class FSMSavingAction(StatesGroup):

    choose_goal = State()
    input_money = State()
