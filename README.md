# Telegram-бот записи в салон (MVP)

## Как запустить

1. Скопируй файл `.env.example` → `.env`
2. Вставь в `.env`:
   - BOT_TOKEN (получи у @BotFather)
   - ADMIN_ID (твой Telegram ID, можно узнать у @userinfobot)

3. Установи зависимости:
```bash
pip install -r requirements.txt
```

4. Запусти:
```bash
python main.py
```

## Команды админа
- `/bookings` — посмотреть все записи

## Структура
```
salon_bot/
├── main.py
├── config.py
├── states.py
├── database.py
├── requirements.txt
├── .env
├── handlers/
│   ├── start.py
│   ├── booking.py
│   └── admin.py
└── keyboards/
    └── inline.py
```
