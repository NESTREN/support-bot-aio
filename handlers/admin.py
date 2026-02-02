from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from states import AdminFSM
from database import *
from keyboards.admin import *
from keyboards.user import photo_kb
from config import ADMINS

router = Router()

@router.message(F.text=="/admin")
async def admin(m: Message):
    await m.answer("Админ-панель", reply_markup=admin_menu())

@router.callback_query(F.data=="a_users")
async def users(c: CallbackQuery):
    users = await get_users()
    if not users:
        await c.message.answer("Нет пользователей")
    for uid, username in users:
        await c.message.answer(f"👤 @{username or 'без username'}\nID: {uid}\n🔗 tg://user?id={uid}")
    await c.answer()

@router.callback_query(F.data=="a_stats")
async def stats(c: CallbackQuery):
    t,o,w,cl = await get_stats()
    await c.message.answer(f"📊 Всего: {t}\n🆕: {o}\n🟡: {w}\n✅: {cl}")
    await c.answer()

@router.callback_query(F.data=="a_open")
async def open_list(c: CallbackQuery):
    for t in await get_tickets("open"):
        await c.message.answer(f"🎫 #{t[0]}", reply_markup=ticket_kb(t[0]))
    await c.answer()

@router.callback_query(F.data=="a_work")
async def work_list(c: CallbackQuery):
    for t in await get_tickets("in_work"):
        await c.message.answer(f"🎫 #{t[0]} (в работе)", reply_markup=ticket_kb(t[0]))
    await c.answer()

@router.callback_query(F.data.startswith("a_work_set:"))
async def work_set(c: CallbackQuery):
    await set_status(int(c.data.split(":")[1]),"in_work")
    uid = (await get_tickets())[int(c.data.split(":")[1])-1][1]
    await c.bot.send_message(uid,"🟡 Ваш тикет взят в работу")
    await c.answer("В работе", show_alert=True)

@router.callback_query(F.data.startswith("a_close:"))
async def close(c: CallbackQuery):
    await set_status(int(c.data.split(":")[1]),"closed")
    uid = (await get_tickets())[int(c.data.split(":")[1])-1][1]
    await c.bot.send_message(uid,"✅ Ваш тикет закрыт")
    await c.answer("Закрыт", show_alert=True)

@router.callback_query(F.data.startswith("a_hist:"))
async def hist(c: CallbackQuery):
    for mid,s,t,f in await get_messages(int(c.data.split(":")[1])):
        if f:
            await c.message.answer(f"{s}: 📷 Фото", reply_markup=photo_kb(mid))
        else:
            await c.message.answer(f"{s}: {t}")
    await c.answer()

@router.callback_query(F.data.startswith("a_ans:"))
async def ans(c: CallbackQuery, state: FSMContext):
    await state.update_data(tid=int(c.data.split(":")[1]))
    await state.set_state(AdminFSM.answer)
    await c.message.answer("Введите текст или фото")
    await c.answer()

@router.message(AdminFSM.answer, F.photo)
async def admin_photo(m: Message, state: FSMContext):
    tid = (await state.get_data())["tid"]
    await add_message(tid,"admin",file_id=m.photo[-1].file_id)
    uid = (await get_tickets())[tid-1][1]
    await m.bot.send_photo(uid,m.photo[-1].file_id,caption="📷 Ответ поддержки")
    await m.answer("Фото отправлено")
    await state.clear()

@router.message(AdminFSM.answer)
async def admin_text(m: Message, state: FSMContext):
    tid = (await state.get_data())["tid"]
    await add_message(tid,"admin",text=m.text)
    uid = (await get_tickets())[tid-1][1]
    await m.bot.send_message(uid,f"💬 Ответ поддержки:\n{m.text}")
    await m.answer("Ответ отправлен")
    await state.clear()

@router.callback_query(F.data=="a_export")
async def export_all(c: CallbackQuery):
    tickets = await get_tickets()
    text = "\n".join([f"#{t[0]} | user {t[1]} | {t[2]}" for t in tickets])
    await c.message.answer(text or "Нет данных")
    await c.answer()

@router.callback_query(F.data.startswith("a_export_ticket:"))
async def export_ticket(c: CallbackQuery):
    tid = int(c.data.split(":")[1])
    msgs = await get_messages(tid)
    out = []
    for _,s,t,f in msgs:
        out.append(f"{s}: {'[photo]' if f else t}")
    await c.message.answer("\n".join(out) or "Пусто")
    await c.answer()