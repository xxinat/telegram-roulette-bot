"""
Обработчик главного меню
"""

from aiogram import Router, F
from aiogram.types import CallbackQuery
from database.db_json import user_manager
from utils.keyboards import (
    get_main_menu_keyboard, get_shop_keyboard, get_roulette_keyboard,
    get_free_bear_keyboard
)

router = Router()


@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery):
    """Вернуться в главное меню"""
    user = user_manager.get_user(callback.from_user.id)
    
    if not user:
        await callback.answer("❌ Ошибка: пользователь не найден", show_alert=True)
        return
    
    await callback.message.edit_text(
        f"👋 <b>Главное меню</b>\n\n"
        f"Выберите что вы хотите сделать:",
        reply_markup=get_main_menu_keyboard(),
        parse_mode="HTML"
    )


@router.callback_query(F.data == "shop")
async def shop_menu(callback: CallbackQuery):
    """Открыть магазин подарков"""
    user = user_manager.get_user(callback.from_user.id)
    
    if not user:
        await callback.answer("❌ Ошибка: пользователь не найден", show_alert=True)
        return
    
    await callback.message.edit_text(
        f"🎁 <b>МАГАЗИН ПОДАРКОВ</b>\n\n"
        f"⏳ <b>В ДАННЫЙ МОМЕНТ НЕДОСТУПНО</b>\n\n"
        f"Приносим извинения, функция магазина подарков временно закрыта.\n"
        f"Пожалуйста, возвращайтесь позже! 😊",
        reply_markup=get_main_menu_keyboard(),
        parse_mode="HTML"
    )


@router.callback_query(F.data == "roulette")
async def roulette_menu(callback: CallbackQuery):
    """Открыть рулетку"""
    user = user_manager.get_user(callback.from_user.id)
    
    if not user:
        await callback.answer("❌ Ошибка: пользователь не найден", show_alert=True)
        return
    
    await callback.message.edit_text(
        f"🎡 <b>РУЛЕТКА - Низкие шансы!</b>\n\n"
        f"🎰 <b>Как работает:</b>\n"
        f"• Выбери билет (низкий до высокий шанс)\n"
        f"• Рискни своими звёздами\n"
        f"• Выигрыш только подарки Telegram 🎁\n\n"
        f"Выбери билет:",
        reply_markup=get_roulette_keyboard(),
        parse_mode="HTML"
    )


@router.callback_query(F.data == "profile")
async def profile_menu(callback: CallbackQuery):
    """Открыть профиль"""
    user = user_manager.get_user(callback.from_user.id)
    
    if not user:
        await callback.answer("❌ Ошибка: пользователь не найден", show_alert=True)
        return
    
    username_text = f"@{user['username']}" if user['username'] else "Не указано"
    withdrawn_gifts = user.get('withdrawn_gifts', 0)
    pending_withdrawal = user_manager.get_user_pending_withdrawal(callback.from_user.id)
    
    await callback.message.edit_text(
        f"👤 <b>МОЙ ПРОФИЛЬ</b>\n\n"
        f"👤 <b>Имя:</b> {user['first_name']}\n"
        f"📱 <b>Username:</b> {username_text}\n"
        f"🆔 <b>ID:</b> {user['telegram_id']}\n\n"
        f"⏳ <b>Ожидает вывода:</b> {pending_withdrawal}\n"
        f"✅ <b>Всего выведено:</b> {withdrawn_gifts}\n\n"
        f"🔗 <b>Реф. код:</b> <code>{user['referral_code']}</code>\n"
        f"👥 <b>Приглашено:</b> {user.get('total_referrals', 0)} чел.\n",
        reply_markup=get_main_menu_keyboard(),
        parse_mode="HTML"
    )
