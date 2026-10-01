from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from config import ADMIN_ID
from database import get_all_bookings

router = Router()


def admin_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📅 Сегодня", callback_data="admin_today"),
         InlineKeyboardButton(text="📆 Завтра", callback_data="admin_tomorrow")],
        [InlineKeyboardButton(text="📋 Все записи", callback_data="admin_all")]
    ])


def format_booking(b):
    return (
        f"#{b['id']} | <b>{b['service']}</b>\n"
        f"👩‍🎨 {b.get('master', '—')}\n"
        f"📅 {b['date']}  🕐 {b['time']}\n"
        f"👤 {b['name']}\n"
        f"📱 {b['phone']}\n"
        f"Статус: {b.get('status', 'new')}\n"
    )


@router.message(Command("bookings"), F.from_user.id == ADMIN_ID)
async def show_bookings(message: Message):
    await message.answer("⚙️ <b>Панель записей</b>", reply_markup=admin_kb())


async def send_filtered(message: Message, mode: str):
    from datetime import datetime, timedelta
    bookings = await get_all_bookings()
    today = datetime.now()
    target = today if mode == "today" else today + timedelta(days=1)
    target_str = target.strftime("%d.%m")
    if mode == "all":
        selected = bookings[:30]
    else:
        selected = [b for b in bookings if b["date"] == target_str]

    if not selected:
        await message.answer("Записей нет.")
        return
    await message.answer("\n".join(format_booking(b) for b in selected))


@router.callback_query(F.data.in_({"admin_today", "admin_tomorrow", "admin_all"}), F.from_user.id == ADMIN_ID)
async def admin_filter(callback: CallbackQuery):
    mode = {"admin_today": "today", "admin_tomorrow": "tomorrow", "admin_all": "all"}[callback.data]
    await send_filtered(callback.message, mode)
    await callback.answer()
