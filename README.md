# 🤖 support-bot-aio

Полноценная система поддержки пользователей (support / helpdesk),  
реализованная **полностью внутри Telegram** с использованием Python.

---

## 🛠 Стек технологий
![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![aiogram](https://img.shields.io/badge/aiogram-async-green)
![Telegram](https://img.shields.io/badge/Telegram-Bot-blue?logo=telegram)
![License](https://img.shields.io/badge/License-Apache%202.0-green)

---

## 🚀 Возможности
- 📩 Приём сообщений от пользователей
- 🧑‍💼 Система поддержки (операторы / администраторы)
- 🔄 Асинхронная обработка событий
- 🧠 FSM (машина состояний)
- ⌨️ Inline / Reply клавиатуры
- 📦 Гибкая структура проекта

---

## 📁 Структура проекта
```text
support-bot-aio/
│
├── handlers/        # Хендлеры сообщений
├── keyboards/       # Клавиатуры
├── states.py        # FSM состояния
├── bot.py           # Точка входа
├── config.py        # Конфигурация
├── requirements.txt
└── README.md
