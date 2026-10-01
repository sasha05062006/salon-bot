# Настройки конкретного салона.
# При подключении нового салона меняется в первую очередь этот файл.

SALON = {
    "name": "Ваш салон",
    "description": "Салон красоты",
    "address": "г. Ташкент, ул. Примерная, 15",
    "phone": "+998 90 123 45 67",
    "telegram": "@your_salon",
    "work_hours": "10:00 – 20:00",
    "masters": {\n        "master_1": {"ru": "Анна", "uz": "Anna"},\n        "master_2": {"ru": "Мария", "uz": "Maria"},\n    },\n    "services": {
        "haircut": {
            "ru": "Стрижка",
            "uz": "Soch olish",
            "price": "80 000 сум",
            "duration": 60,
        },
        "manicure": {
            "ru": "Маникюр",
            "uz": "Manikyur",
            "price": "120 000 сум",
            "duration": 60,
        },
        "coloring": {
            "ru": "Окрашивание",
            "uz": "Bo‘yash",
            "price": "250 000 сум",
            "duration": 120,
        },
        "styling": {
            "ru": "Укладка",
            "uz": "Ukladka",
            "price": "100 000 сум",
            "duration": 60,
        },
    },
}
