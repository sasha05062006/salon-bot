from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from states import BookingStates
from keyboards.inline import services_kb, dates_kb, times_kb, main_menu, cancel_kb
from database import add_booking
from config import ADMIN_ID
from locales.texts import t

router = Router()


@router.message(F.text.in_({"📅 Записаться", "📅 Yozilish"}))
async def start_booking(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    
    await state.set_state(BookingStates.waiting_for_service)
    await message.answer(t(lang, "choose_service"), reply_markup=services_kb(lang))


@router.callback_query(F.data.startswith("service_"))
async def process_service(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    
    service_key = callback.data.split("_")[1]
    service_name = t(lang, "services")[service_key]
    
    await state.update_data(service=service_name, service_key=service_key)
    await state.set_state(BookingStates.waiting_for_date)
    
    await callback.message.edit_text(
        f"{t(lang, 'choose_service')}\n\n✅ {service_name}\n\n{t(lang, 'choose_date')}",
        reply_markup=dates_kb(lang)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("date_"))
async def process_date(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    
    date = callback.data.split("_")[1]
    await state.update_data(date=date)
    await state.set_state(BookingStates.waiting_for_time)
    
    await callback.message.edit_text(
        f"✅ {data.get('service')}\n📅 {date}\n\n{t(lang, 'choose_time')}",
        reply_markup=times_kb(lang)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("time_"))
async def process_time(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    
    time = callback.data.split("_")[1]
    await state.update_data(time=time)
    await state.set_state(BookingStates.waiting_for_name)
    
    await callback.message.edit_text(
        f"✅ {data.get('service')}\n📅 {data.get('date')}  {time}\n\n{t(lang, 'enter_name')}"
    )
    await callback.message.answer(t(lang, "enter_name"), reply_markup=cancel_kb(lang))
    await callback.answer()


@router.message(BookingStates.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    
    if message.text in [t("ru", "btn_cancel"), t("uz", "btn_cancel")]:
        await state.set_state(None)
        await message.answer(t(lang, "booking_cancelled"), reply_markup=main_menu(lang))
        return
    
    await state.update_data(name=message.text)
    await state.set_state(BookingStates.waiting_for_phone)
    await message.answer(t(lang, "enter_phone"))


@router.message(BookingStates.waiting_for_phone)
async def process_phone(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    
    if message.text in [t("ru", "btn_cancel"), t("uz", "btn_cancel")]:
        await state.set_state(None)
        await message.answer(t(lang, "booking_cancelled"), reply_markup=main_menu(lang))
        return
    
    phone = message.text
    name = data.get("name")
    service = data.get("service")
    date = data.get("date")
    time = data.get("time")
    
    await add_booking(
        user_id=message.from_user.id,
        username=message.from_user.username or "",
        service=service,
        date=date,
        time=time,
        name=name,
        phone=phone,
        lang=lang
    )
    
    # Уведомление админу
    text_admin = (
        f"🆕 <b>Новая запись!</b>\n\n"
        f"Услуга: {service}\n"
        f"Дата: {date}\n"
        f"Время: {time}\n"
        f"Имя: {name}\n"
        f"Телефон: {phone}\n"
        f"Язык: {lang}\n"
        f"Username: @{message.from_user.username or 'нет'}"
    )
    try:
        await message.bot.send_message(ADMIN_ID, text_admin)
    except Exception:
        pass
    
    await message.answer(
        t(lang, "booking_success", service=service, date=date, time=time, name=name, phone=phone),
        reply_markup=main_menu(lang)
    )
    await state.set_state(None)


@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    await state.set_state(None)
    await callback.message.delete()
    await callback.message.answer(t(lang, "main_menu"), reply_markup=main_menu(lang))
    await callback.answer()


@router.callback_query(F.data == "back_to_services")
async def back_to_services(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    await state.set_state(BookingStates.waiting_for_service)
    await callback.message.edit_text(t(lang, "choose_service"), reply_markup=services_kb(lang))
    await callback.answer()


@router.callback_query(F.data == "back_to_dates")
async def back_to_dates(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    await state.set_state(BookingStates.waiting_for_date)
    await callback.message.edit_text(
        f"✅ {data.get('service')}\n\n{t(lang, 'choose_date')}",
        reply_markup=dates_kb(lang)
    )
    await callback.answer()
