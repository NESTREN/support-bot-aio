from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def user_kb():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="🎫 Новый тикет")],
        [KeyboardButton(text="📄 Мой тикет"), KeyboardButton(text="ℹ Помощь")]
    ], resize_keyboard=True)

def reply_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✍ Ответить", callback_data="u_reply")]
    ])

def photo_kb(mid):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📷 Открыть фото", callback_data=f"open_photo:{mid}")]
    ])