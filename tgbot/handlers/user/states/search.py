from aiogram.fsm.state import State, StatesGroup


class SearchSG(StatesGroup):
    search = State()
    detail = State()
    comment = State()
    add_comment = State()
