from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📅 Записаться")],
            [KeyboardButton(text="📋 Прайс"), KeyboardButton(text="📍 Адрес")],
            [KeyboardButton(text="📞 Контакты")]
        ],
        resize_keyboard=True
    )


def services_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Стрижка", callback_data="service_стрижка")],
        [InlineKeyboardButton(text="Маникюр", callback_data="service_маникюр")],
        [InlineKeyboardButton(text="Окрашивание", callback_data="service_окрашивание")],
        [InlineKeyboardButton(text="Укладка", callback_data="service_укладка")],
        [InlineKeyboardButton(text="« Назад", callback_data="back_to_menu")]
    ])


def cancel_kb():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Отмена")]],
        resize_keyboard=True
    )
