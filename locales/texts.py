TEXTS = {
    "ru": {
        "welcome": "👋 Добро пожаловать!\n\nЯ бот для записи в салон красоты.\nВыберите язык / Tilni tanlang:",
        "choose_lang": "Выберите язык:",
        "main_menu": "Главное меню:",
        "btn_book": "📅 Записаться",
        "btn_price": "📋 Прайс",
        "btn_address": "📍 Адрес",
        "btn_contacts": "📞 Контакты",
        "btn_back": "« Назад",
        "btn_cancel": "❌ Отмена",
        "choose_service": "Выберите услугу:",
        "choose_date": "Выберите дату:",
        "choose_time": "Выберите время:",
        "enter_name": "Введите ваше имя:",
        "enter_phone": "Введите номер телефона:",
        "booking_success": "✅ Запись успешно создана!\n\nУслуга: <b>{service}</b>\nДата: {date}\nВремя: {time}\nИмя: {name}\nТелефон: {phone}\n\nМы свяжемся с вами для подтверждения.",
        "booking_cancelled": "Запись отменена.",
        "price_list": "<b>Прайс-лист:</b>\n\n• Стрижка — 80 000 сум\n• Маникюр — 120 000 сум\n• Окрашивание — 250 000 сум\n• Укладка — 100 000 сум",
        "address": "📍 Адрес: г. Ташкент, ул. Примерная, 15\n\nРежим работы: 10:00 – 20:00",
        "contacts": "📞 Телефон: +998 90 123 45 67\nTelegram: @your_salon",
        "services": {
            "haircut": "Стрижка",
            "manicure": "Маникюр",
            "coloring": "Окрашивание",
            "styling": "Укладка"
        }
    },
    "uz": {
        "welcome": "👋 Xush kelibsiz!\n\nMen go‘zallik saloniga yozilish botiman.\nTilni tanlang / Выберите язык:",
        "choose_lang": "Tilni tanlang:",
        "main_menu": "Asosiy menyu:",
        "btn_book": "📅 Yozilish",
        "btn_price": "📋 Narxlar",
        "btn_address": "📍 Manzil",
        "btn_contacts": "📞 Kontaktlar",
        "btn_back": "« Orqaga",
        "btn_cancel": "❌ Bekor qilish",
        "choose_service": "Xizmatni tanlang:",
        "choose_date": "Sanani tanlang:",
        "choose_time": "Vaqtni tanlang:",
        "enter_name": "Ismingizni kiriting:",
        "enter_phone": "Telefon raqamingizni kiriting:",
        "booking_success": "✅ Yozuv muvaffaqiyatli yaratildi!\n\nXizmat: <b>{service}</b>\nSana: {date}\nVaqt: {time}\nIsm: {name}\nTelefon: {phone}\n\nTasdiqlash uchun siz bilan bog‘lanamiz.",
        "booking_cancelled": "Yozuv bekor qilindi.",
        "price_list": "<b>Narxlar ro‘yxati:</b>\n\n• Soch olish — 80 000 so‘m\n• Manikyur — 120 000 so‘m\n• Bo‘yash — 250 000 so‘m\n• Ukladka — 100 000 so‘m",
        "address": "📍 Manzil: Toshkent sh., Namunaviy ko‘chasi, 15\n\nIsh vaqti: 10:00 – 20:00",
        "contacts": "📞 Telefon: +998 90 123 45 67\nTelegram: @your_salon",
        "services": {
            "haircut": "Soch olish",
            "manicure": "Manikyur",
            "coloring": "Bo‘yash",
            "styling": "Ukladka"
        }
    }
}


def t(lang: str, key: str, **kwargs):
    text = TEXTS.get(lang, TEXTS["ru"]).get(key, key)
    if kwargs:
        return text.format(**kwargs)
    return text
