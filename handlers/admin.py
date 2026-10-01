from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from config import ADMIN_ID
from database import get_all_bookings

router = Router()


@router.message(Command("bookings"), F.from_user.id == ADMIN_ID)
async def show_bookings(message: Message):
    bookings = await get_all_bookings()
    if not bookings:
        await message.answer("Записей пока нет.")
        return

    text = "<b>Последние записи:</b>\n\n"
    for b in bookings[:15]:
        text += (
            f"#{b['id']} | {b['service']}\n"
            f"{b['date']} {b['time']} — {b['name']} ({b['phone']})\n"
            f"Статус: {b['status']}\n\n"
        )
    await message.answer(text)
