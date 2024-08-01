from aiogram.fsm.state import State, StatesGroup


class FSMInputLimit(StatesGroup):

    limit = State()
