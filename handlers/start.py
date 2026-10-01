from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from keyboards.inline import language_kb, main_menu
from locales.texts import t
from states import BookingStates

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(BookingStates.choosing_language)
    await message.answer(
        t("ru", "welcome"),
        reply_markup=language_kb()
    )


@router.callback_query(F.data.startswith("lang_"))
async def set_language(callback: CallbackQuery, state: FSMContext):
    lang = callback.data.split("_")[1]
    await state.update_data(lang=lang)
    await state.set_state(None)
    
    await callback.message.edit_text(t(lang, "main_menu"))
    await callback.message.answer(
        t(lang, "main_menu"),
        reply_markup=main_menu(lang)
    )
    await callback.answer()


@router.message(F.text.in_({"📋 Прайс", "📋 Narxlar"}))
async def show_price(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    await message.answer(t(lang, "price_list"))


@router.message(F.text.in_({"📍 Адрес", "📍 Manzil"}))
async def show_address(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    await message.answer(t(lang, "address"))


@router.message(F.text.in_({"📞 Контакты", "📞 Kontaktlar"}))
async def show_contacts(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    await message.answer(t(lang, "contacts"))
