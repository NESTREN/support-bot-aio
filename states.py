from aiogram.fsm.state import StatesGroup, State

class UserFSM(StatesGroup):
    new_ticket = State()
    reply = State()

class AdminFSM(StatesGroup):
    answer = State()