"""
Админ панель бота
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from config import ADMIN_IDS
from database.db_json import user_manager
from utils.keyboards import InlineKeyboardMarkup, InlineKeyboardButton

router = Router()


def is_admin(user_id: int) -> bool:
    """Проверить является ли пользователь админом"""
    return user_id in ADMIN_IDS


@router.message(Command("admin"))
async def admin_panel(message: Message):
    """Главная администраторская панель"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ У вас нет доступа к админ панели")
        return
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats")],
        [InlineKeyboardButton(text="💰 Запросы на вывод", callback_data="admin_withdrawals")],
        [InlineKeyboardButton(text="🎰 Выигрыши рулетки", callback_data="admin_roulette_wins")],
        [InlineKeyboardButton(text="👥 Список пользователей", callback_data="admin_users")],
    ])
    
    await message.answer(
        "🔐 <b>Админ Панель</b>\n\n"
        "Выберите действие:",
        reply_markup=keyboard,
        parse_mode="HTML"
    )


@router.callback_query(F.data == "admin_stats")
async def admin_stats(callback: CallbackQuery):
    """Показать статистику"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Доступ запрещен", show_alert=True)
        return
    
    users_count = len(user_manager.get_all_users())
    
    total_referrals = 0
    total_bears = 0
    for user in user_manager.get_all_users():
        total_referrals += user.get('total_referrals', 0)
        total_bears += user.get('bears', 0)
    
    text = f"""
📊 <b>Статистика Бота</b>

👥 Всего пользователей: <b>{users_count}</b>
🔗 Всего рефералов: <b>{total_referrals}</b>
🐻 Всего подарков в системе: <b>{total_bears}</b>
"""
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_back")],
    ])
    
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")


@router.callback_query(F.data == "admin_withdrawals")
async def admin_withdrawals(callback: CallbackQuery):
    """Показать запросы на вывод подарков"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Доступ запрещен", show_alert=True)
        return
    
    withdrawals = user_manager.get_pending_withdrawals()
    
    if not withdrawals:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_back")],
        ])
        
        await callback.message.edit_text(
            "✅ Нет ожидающих запросов на вывод",
            reply_markup=keyboard,
            parse_mode="HTML"
        )
        return
    
    text = "💰 <b>Запросы на вывод подарков</b>\n\n"
    keyboard_buttons = []
    
    for withdrawal in withdrawals:
        user_id = withdrawal['user_id']
        user = user_manager.get_user(user_id)
        amount = withdrawal['amount']
        
        text += f"""
👤 <b>Пользователь:</b> @{user.get('username', 'нет')} ({user.get('first_name', 'Не указано')})
💰 <b>Количество подарков:</b> {amount}
📱 <b>ID:</b> {user_id}
⏰ <b>Дата:</b> {withdrawal.get('created_at', 'неизвестна')}
━━━━━━━━━━━━━━━━
"""
        
        keyboard_buttons.append([
            InlineKeyboardButton(text="✅ Одобрить", callback_data=f"approve_withdrawal_{user_id}"),
            InlineKeyboardButton(text="❌ Отклонить", callback_data=f"reject_withdrawal_{user_id}")
        ])
    
    keyboard_buttons.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_back")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
    
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")


@router.callback_query(F.data == "admin_users")
async def admin_users(callback: CallbackQuery):
    """Показать список пользователей"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Доступ запрещен", show_alert=True)
        return
    
    users = user_manager.get_all_users()
    
    text = "👥 <b>Список Пользователей</b>\n\n"
    
    for user in users[:10]:  # Первые 10 пользователей
        text += f"""
👤 <b>{user.get('first_name', 'Без имени')}</b> @{user.get('username', 'нет username')}
├ ID: {user['telegram_id']}
├ 🎁 Подарков: {user.get('bears', 0)}
├ 🔗 Рефералов: {user.get('total_referrals', 0)}
├ ✅ Активных: {user.get('active_referrals', 0)}
└ 📱 Зарегистрирован: {user.get('created_at', 'неизвестно')[:10]}

"""
    
    if len(users) > 10:
        text += f"\n... и еще {len(users) - 10} пользователей"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_back")],
    ])
    
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")


@router.callback_query(F.data.startswith("approve_withdrawal_"))
async def approve_withdrawal(callback: CallbackQuery):
    """Одобрить вывод"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Доступ запрещен", show_alert=True)
        return
    
    # Парсим user_id из callback_data
    user_id = int(callback.data.replace("approve_withdrawal_", ""))
    
    # Отметить вывод как одобренный
    user_manager.approve_withdrawal(user_id)
    
    user = user_manager.get_user(user_id)
    
    await callback.answer(f"✅ Вывод одобрен для @{user.get('username', 'пользователя')}", show_alert=True)
    
    # Обновить уведомление
    await callback.message.edit_text(
        f"✅ <b>ВЫВОД ОДОБРЕН</b>\n\n"
        f"👤 Пользователь: @{user.get('username', 'нет username')}\n"
        f"🆔 ID: {user_id}\n"
        f"⏳ Статус: <b>ОДОБРЕНО</b>",
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("reject_withdrawal_"))
async def reject_withdrawal(callback: CallbackQuery):
    """Отклонить вывод"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Доступ запрещен", show_alert=True)
        return
    
    # Парсим user_id из callback_data
    user_id = int(callback.data.replace("reject_withdrawal_", ""))
    
    # Отметить вывод как отклоненный
    user_manager.reject_withdrawal(user_id)
    
    user = user_manager.get_user(user_id)
    
    await callback.answer(f"❌ Вывод отклонен для @{user.get('username', 'пользователя')}", show_alert=True)
    
    # Обновить уведомление
    await callback.message.edit_text(
        f"❌ <b>ВЫВОД ОТКЛОНЕН</b>\n\n"
        f"👤 Пользователь: @{user.get('username', 'нет username')}\n"
        f"🆔 ID: {user_id}\n"
        f"⏳ Статус: <b>ОТКЛОНЕНО</b>",
        parse_mode="HTML"
    )
    await admin_withdrawals(callback)


@router.callback_query(F.data == "admin_back")
async def admin_back(callback: CallbackQuery):
    """Вернуться в главное меню админ панели"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Доступ запрещен", show_alert=True)
        return
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats")],
        [InlineKeyboardButton(text="💰 Запросы на вывод", callback_data="admin_withdrawals")],
        [InlineKeyboardButton(text="🎰 Выигрыши рулетки", callback_data="admin_roulette_wins")],
        [InlineKeyboardButton(text="👥 Список пользователей", callback_data="admin_users")],
    ])
    
    await callback.message.edit_text(
        "🔐 <b>Админ Панель</b>\n\n"
        "Выберите действие:",
        reply_markup=keyboard,
        parse_mode="HTML"
    )


@router.callback_query(F.data == "admin_roulette_wins")
async def admin_roulette_wins(callback: CallbackQuery):
    """Показать выигрыши из рулетки"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Доступ запрещен", show_alert=True)
        return
    
    wins = user_manager.get_pending_roulette_wins()
    
    if not wins:
        text = "🎰 <b>Выигрыши рулетки</b>\n\n" \
               "✅ Нет ожидающих выигрышей"
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_back")],
        ])
        
        await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
        return
    
    text = "🎰 <b>Выигрыши из рулетки</b>\n\n"
    keyboard_buttons = []
    
    for win in wins:
        text += f"""
🎁 <b>Приз:</b> {win['prize_name']}
👤 <b>Пользователь:</b> @{win['username']}
🆔 <b>ID:</b> {win['telegram_id']}
📱 <b>Имя:</b> {win['first_name']}
🎫 <b>Билет:</b> {win['ticket_name']}
💰 <b>Стоимость билета:</b> {win['ticket_price']} ⭐
📅 <b>Дата:</b> {win.get('created_at', 'неизвестна')[:10]}
━━━━━━━━━━━━━━━━
"""
        
        keyboard_buttons.append([
            InlineKeyboardButton(text="✅ Отправлено", callback_data=f"approve_roulette_{win['id']}"),
            InlineKeyboardButton(text="❌ Отклонить", callback_data=f"reject_roulette_{win['id']}")
        ])
    
    keyboard_buttons.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_back")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
    
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")


@router.callback_query(F.data.startswith("approve_roulette_"))
async def approve_roulette_win(callback: CallbackQuery):
    """Одобрить выигрыш из рулетки"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Доступ запрещен", show_alert=True)
        return
    
    win_id = int(callback.data.replace("approve_roulette_", ""))
    user_manager.approve_roulette_win(win_id)
    
    # Найти выигрыш в файле
    roulette_wins = user_manager._read_json(user_manager.roulette_wins_file)
    approved_win = next((w for w in roulette_wins if w['id'] == win_id), None)
    
    if approved_win:
        await callback.answer(f"✅ Выигрыш одобрен для @{approved_win['username']}", show_alert=True)
    
    # Обновить список
    await admin_roulette_wins(callback)


@router.callback_query(F.data.startswith("reject_roulette_"))
async def reject_roulette_win(callback: CallbackQuery):
    """Отклонить выигрыш из рулетки"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Доступ запрещен", show_alert=True)
        return
    
    win_id = int(callback.data.replace("reject_roulette_", ""))
    user_manager.reject_roulette_win(win_id)
    
    # Найти выигрыш в файле
    roulette_wins = user_manager._read_json(user_manager.roulette_wins_file)
    rejected_win = next((w for w in roulette_wins if w['id'] == win_id), None)
    
    if rejected_win:
        await callback.answer(f"❌ Выигрыш отклонен для @{rejected_win['username']}", show_alert=True)
    
    # Обновить список
    await admin_roulette_wins(callback)
