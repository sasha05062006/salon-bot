from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from keyboards.inline import main_menu

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "👋 Добро пожаловать!\n\n"
        "Я бот для записи в салон.\n"
        "Выберите действие:",
        reply_markup=main_menu()
    )


@router.message(F.text == "📋 Прайс")
async def show_price(message: Message):
    text = (
        "<b>Прайс-лист:</b>\n\n"
        "• Стрижка — 80 000 сум\n"
        "• Маникюр — 120 000 сум\n"
        "• Окрашивание — 250 000 сум\n"
        "• Укладка — 100 000 сум"
    )
    await message.answer(text)


@router.message(F.text == "📍 Адрес")
async def show_address(message: Message):
    await message.answer("📍 Адрес: г. Ташкент, ул. Примерная, 15\n\nРежим работы: 10:00 – 20:00")


@router.message(F.text == "📞 Контакты")
async def show_contacts(message: Message):
    await message.answer("📞 Телефон: +998 90 123 45 67\nTelegram: @your_salon")
