from aiogram.fsm.state import State, StatesGroup


class RegisterSG(StatesGroup):
    password = State()
