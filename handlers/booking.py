from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from states import BookingStates
from keyboards.inline import services_kb, main_menu, cancel_kb
from database import add_booking
from config import ADMIN_ID

router = Router()


@router.message(F.text == "📅 Записаться")
async def start_booking(message: Message, state: FSMContext):
    await state.set_state(BookingStates.waiting_for_service)
    await message.answer("Выберите услугу:", reply_markup=services_kb())


@router.callback_query(F.data.startswith("service_"))
async def process_service(callback: CallbackQuery, state: FSMContext):
    service = callback.data.split("_")[1]
    await state.update_data(service=service)
    await state.set_state(BookingStates.waiting_for_date)
    await callback.message.edit_text(f"Услуга: <b>{service}</b>\n\nВведите желаемую дату (например: 05.10):")
    await callback.answer()


@router.message(BookingStates.waiting_for_date)
async def process_date(message: Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await state.clear()
        await message.answer("Запись отменена.", reply_markup=main_menu())
        return

    await state.update_data(date=message.text)
    await state.set_state(BookingStates.waiting_for_time)
    await message.answer("Введите желаемое время (например: 15:30):", reply_markup=cancel_kb())


@router.message(BookingStates.waiting_for_time)
async def process_time(message: Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await state.clear()
        await message.answer("Запись отменена.", reply_markup=main_menu())
        return

    await state.update_data(time=message.text)
    await state.set_state(BookingStates.waiting_for_name)
    await message.answer("Введите ваше имя:")


@router.message(BookingStates.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await state.clear()
        await message.answer("Запись отменена.", reply_markup=main_menu())
        return

    await state.update_data(name=message.text)
    await state.set_state(BookingStates.waiting_for_phone)
    await message.answer("Введите номер телефона:")


@router.message(BookingStates.waiting_for_phone)
async def process_phone(message: Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await state.clear()
        await message.answer("Запись отменена.", reply_markup=main_menu())
        return

    data = await state.get_data()
    phone = message.text

    await add_booking(
        user_id=message.from_user.id,
        username=message.from_user.username or "",
        service=data["service"],
        date=data["date"],
        time=data["time"],
        name=data["name"],
        phone=phone
    )

    # Уведомление админу
    text_admin = (
        f"🆕 <b>Новая запись!</b>\n\n"
        f"Услуга: {data['service']}\n"
        f"Дата: {data['date']}\n"
        f"Время: {data['time']}\n"
        f"Имя: {data['name']}\n"
        f"Телефон: {phone}\n"
        f"Username: @{message.from_user.username or 'нет'}"
    )
    await message.bot.send_message(ADMIN_ID, text_admin)

    await message.answer(
        f"✅ Запись успешно создана!\n\n"
        f"Услуга: <b>{data['service']}</b>\n"
        f"Дата: {data['date']}\n"
        f"Время: {data['time']}\n"
        f"Имя: {data['name']}\n"
        f"Телефон: {phone}\n\n"
        f"Мы свяжемся с вами для подтверждения.",
        reply_markup=main_menu()
    )
    await state.clear()


@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await callback.message.answer("Главное меню:", reply_markup=main_menu())
    await callback.answer()
