from aiogram.dispatcher.filters.state import State, StatesGroup


class BuyCourse(StatesGroup):
    receipt = State()