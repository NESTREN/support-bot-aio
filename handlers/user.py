from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from states import UserFSM
from database import *
from keyboards.user import *
from config import ADMINS

router = Router()

@router.message(F.text=="/start")
async def start(m: Message):
    await add_user(m.from_user.id, m.from_user.username)
    await m.answer("Поддержка", reply_markup=user_kb())

@router.message(F.text=="🎫 Новый тикет")
async def new_ticket(m: Message, state: FSMContext):
    await m.answer("Опишите проблему")
    await state.set_state(UserFSM.new_ticket)

@router.message(UserFSM.new_ticket)
async def create(m: Message, state: FSMContext):
    tid = await create_ticket(m.from_user.id)
    await add_message(tid,"user",text=m.text)
    for a in ADMINS:
        await m.bot.send_message(a,f"🆕 Новый тикет #{tid}")
    await m.answer("Тикет создан", reply_markup=user_kb())
    await state.clear()

@router.message(F.photo)
async def photo(m: Message):
    tid = await get_active_ticket(m.from_user.id)
    if not tid:
        return
    await add_message(tid,"user",file_id=m.photo[-1].file_id)
    for a in ADMINS:
        await m.bot.send_photo(a,m.photo[-1].file_id,caption="📷 Фото от пользователя")

@router.message(F.text=="📄 Мой тикет")
async def my_ticket(m: Message):
    tid = await get_active_ticket(m.from_user.id)
    if not tid:
        await m.answer("Нет активных тикетов")
        return
    msgs = await get_messages(tid)
    for i,(mid,s,t,f) in enumerate(msgs):
        last = i == len(msgs)-1
        if f:
            await m.answer(f"{s}: 📷 Фото", reply_markup=reply_kb() if last else photo_kb(mid))
        else:
            await m.answer(f"{s}: {t}", reply_markup=reply_kb() if last else None)

@router.callback_query(F.data=="u_reply")
async def reply_start(c: CallbackQuery, state: FSMContext):
    await state.set_state(UserFSM.reply)
    await c.message.answer("Введите сообщение")
    await c.answer()

@router.message(UserFSM.reply)
async def reply_send(m: Message, state: FSMContext):
    tid = await get_active_ticket(m.from_user.id)
    await add_message(tid,"user",text=m.text)
    for a in ADMINS:
        await m.bot.send_message(a,f"💬 Ответ пользователя #{tid}: {m.text}")
    await m.answer("Отправлено", reply_markup=user_kb())
    await state.clear()

@router.callback_query(F.data.startswith("open_photo:"))
async def open_photo(c: CallbackQuery):
    fid = await get_file_id(int(c.data.split(":")[1]))
    if fid:
        await c.message.answer_photo(fid)
    await c.answer()