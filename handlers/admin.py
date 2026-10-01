from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from config import ADMIN_ID
from database import get_all_bookings, update_booking_status, get_booking, get_services, get_masters, add_service, deactivate_service, add_master, deactivate_master

router = Router()


def admin_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📅 Сегодня", callback_data="admin_today"),
         InlineKeyboardButton(text="📆 Завтра", callback_data="admin_tomorrow")],
        [InlineKeyboardButton(text="📋 Все записи", callback_data="admin_all")],
        [InlineKeyboardButton(text="💇 Услуги", callback_data="catalog_services"),
         InlineKeyboardButton(text="👩‍🎨 Мастера", callback_data="catalog_masters")]
    ])


def booking_actions(booking_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Подтвердить", callback_data=f"booking_confirm_{booking_id}"),
            InlineKeyboardButton(text="❌ Отменить", callback_data=f"booking_cancel_{booking_id}")
        ]
    ])


def format_booking(b):
    status = {"new": "🆕 Новая", "confirmed": "✅ Подтверждена", "cancelled": "❌ Отменена"}.get(b.get("status"), b.get("status", "new"))
    return (
        f"#{b['id']} | <b>{b['service']}</b>\n"
        f"👩‍🎨 {b.get('master', '—')}\n"
        f"📅 {b['date']}  🕐 {b['time']}\n"
        f"👤 {b['name']}\n"
        f"📱 {b['phone']}\n"
        f"{status}"
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
    selected = bookings[:30] if mode == "all" else [b for b in bookings if b["date"] == target_str]
    if not selected:
        await message.answer("Записей нет.")
        return
    for b in selected:
        await message.answer(format_booking(b), reply_markup=booking_actions(b["id"]))


@router.callback_query(F.data.in_({"admin_today", "admin_tomorrow", "admin_all"}), F.from_user.id == ADMIN_ID)
async def admin_filter(callback: CallbackQuery):
    mode = {"admin_today": "today", "admin_tomorrow": "tomorrow", "admin_all": "all"}[callback.data]
    await send_filtered(callback.message, mode)
    await callback.answer()


@router.callback_query(F.data.startswith("booking_confirm_"), F.from_user.id == ADMIN_ID)
async def confirm_booking(callback: CallbackQuery):
    booking_id = int(callback.data.rsplit("_", 1)[1])
    booking = await get_booking(booking_id)
    if not booking:
        await callback.answer("Запись не найдена", show_alert=True)
        return
    await update_booking_status(booking_id, "confirmed")
    await callback.message.edit_reply_markup(reply_markup=None)
    try:
        await callback.bot.send_message(
            booking["user_id"],
            f"✅ <b>Ваша запись подтверждена!</b>\n\n"
            f"{booking['service']}\n"
            f"👩‍🎨 {booking.get('master', '—')}\n"
            f"📅 {booking['date']}  🕐 {booking['time']}"
        )
    except Exception:
        pass
    await callback.answer("Подтверждено")


@router.callback_query(F.data.startswith("booking_cancel_"), F.from_user.id == ADMIN_ID)
async def cancel_booking(callback: CallbackQuery):
    booking_id = int(callback.data.rsplit("_", 1)[1])
    booking = await get_booking(booking_id)
    if not booking:
        await callback.answer("Запись не найдена", show_alert=True)
        return
    await update_booking_status(booking_id, "cancelled")
    await callback.message.edit_reply_markup(reply_markup=None)
    try:
        await callback.bot.send_message(
            booking["user_id"],
            f"❌ <b>Ваша запись отменена.</b>\n\n"
            f"{booking['service']}\n"
            f"👩‍🎨 {booking.get('master', '—')}\n"
            f"📅 {booking['date']}  🕐 {booking['time']}"
        )
    except Exception:
        pass
    await callback.answer("Отменено")


@router.callback_query(F.data == "catalog_services", F.from_user.id == ADMIN_ID)
async def catalog_services(callback: CallbackQuery):
    services = await get_services()
    if not services:
        await callback.message.answer("Услуг пока нет.")
    for s in services:
        await callback.message.answer(
            f"💇 <b>{s['name_ru']}</b> / {s['name_uz']}\n"
            f"💰 {s['price']} • ⏱ {s['duration']} мин.",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(text="🗑 Отключить", callback_data=f"service_off_{s['key']}")
            ]])
        )
    await callback.answer()

@router.callback_query(F.data == "catalog_masters", F.from_user.id == ADMIN_ID)
async def catalog_masters(callback: CallbackQuery):
    masters = await get_masters()
    if not masters:
        await callback.message.answer("Мастеров пока нет.")
    for m in masters:
        await callback.message.answer(
            f"👩‍🎨 <b>{m['name_ru']}</b> / {m['name_uz']}",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(text="🗑 Отключить", callback_data=f"master_off_{m['key']}")
            ]])
        )
    await callback.answer()

@router.callback_query(F.data.startswith("service_off_"), F.from_user.id == ADMIN_ID)
async def service_off(callback: CallbackQuery):
    await deactivate_service(callback.data[len("service_off_"):])
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer("Услуга отключена")

@router.callback_query(F.data.startswith("master_off_"), F.from_user.id == ADMIN_ID)
async def master_off(callback: CallbackQuery):
    await deactivate_master(callback.data[len("master_off_"):])
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer("Мастер отключён")
