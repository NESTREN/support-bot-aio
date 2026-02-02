
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def admin_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🆕 Открытые", callback_data="a_open"),
            InlineKeyboardButton(text="🟡 В работе", callback_data="a_work")
        ],
        [
            InlineKeyboardButton(text="📊 Статистика", callback_data="a_stats"),
            InlineKeyboardButton(text="👥 Пользователи", callback_data="a_users")
        ],
        [
            InlineKeyboardButton(text="📤 Экспорт", callback_data="a_export")
        ]
    ])

def ticket_kb(tid):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📜 История", callback_data=f"a_hist:{tid}")],
        [InlineKeyboardButton(text="✍ Ответить", callback_data=f"a_ans:{tid}")],
        [InlineKeyboardButton(text="🟡 В работу", callback_data=f"a_work_set:{tid}")],
        [InlineKeyboardButton(text="✅ Закрыть", callback_data=f"a_close:{tid}")],
        [InlineKeyboardButton(text="📤 Экспорт", callback_data=f"a_export_ticket:{tid}")]
    ])
