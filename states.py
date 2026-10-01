from aiogram.fsm.state import State, StatesGroup


class BookingStates(StatesGroup):
    choosing_language = State()
    waiting_for_service = State()
    waiting_for_master = State()
    waiting_for_date = State()
    waiting_for_time = State()
    waiting_for_name = State()
    waiting_for_phone = State()
