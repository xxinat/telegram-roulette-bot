"""
Реферальная система - приглашение друзей и получение подарков (НОВАЯ ВЕРСИЯ)
"""

from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from database.db_json import user_manager
from datetime import datetime
from utils.keyboards import get_main_menu_keyboard, get_free_bear_keyboard
from config import REFERRAL_COUNT_FOR_GIFT, REFERRAL_GIFT_NAME, ADMIN_IDS

router = Router()


@router.callback_query(F.data == "my_referral_link")
async def show_referral_link(callback: CallbackQuery):
    """Показать реф. ссылку"""
    user = user_manager.get_user(callback.from_user.id)
    
    if not user:
        await callback.answer("❌ Ошибка: пользователь не найден", show_alert=True)
        return
    
    total_refs = user.get('total_referrals', 0)
    active_refs = user.get('active_referrals', 0)
    gifts_earned = user.get('gifts_earned', 0)
    
    # Сколько ещё нужно пригласить для следующего подарка
    refs_to_next_gift = REFERRAL_COUNT_FOR_GIFT - (active_refs % REFERRAL_COUNT_FOR_GIFT)
    
    referral_link = f"https://t.me/testpodarkibotiksbot?start={user['referral_code']}"
    
    text = f"""
🎁 <b>ВАША РЕФЕРАЛЬНАЯ ССЫЛКА</b>

📝 <b>Скопируйте ссылку и отправьте друзьям:</b>
<code>{referral_link}</code>

📊 <b>Ваша статистика:</b>
👥 Всего приглашено: {total_refs} человек
✅ Активных рефералов: {active_refs}
🎁 Подарков получено: {gifts_earned}

🎯 <b>Прогресс к следующему подарку:</b>
{active_refs % REFERRAL_COUNT_FOR_GIFT}/{REFERRAL_COUNT_FOR_GIFT}
Ещё нужно {refs_to_next_gift} рефералов до следующего подарка 🎁
"""
    
    await callback.message.edit_text(text, reply_markup=get_free_bear_keyboard(), parse_mode="HTML")


@router.callback_query(F.data == "my_referrals")
async def show_referrals(callback: CallbackQuery):
    """Показать список приглашений"""
    user = user_manager.get_user(callback.from_user.id)
    
    if not user:
        await callback.answer("❌ Ошибка: пользователь не найден", show_alert=True)
        return
    
    total_refs = user.get('total_referrals', 0)
    active_refs = user.get('active_referrals', 0)
    gifts_earned = user.get('gifts_earned', 0)
    
    text = f"""
👥 <b>МОИ ПРИГЛАШЕНИЯ</b>

📊 <b>Статистика:</b>
• Всего приглашено: {total_refs} человек
• Активных (зарегистрировались): {active_refs}
• Неактивных (не зарегистрировались): {total_refs - active_refs}

🎁 <b>Вознаграждения:</b>
• Получено подарков: {gifts_earned}
• Каждые {REFERRAL_COUNT_FOR_GIFT} активных рефералов = 1 подарок

💡 <b>Как увеличить приглашения:</b>
1. Скопируйте вашу реф. ссылку (кнопка выше)
2. Отправьте её друзьям в Telegram
3. Когда друг перейдёт по ссылке и нажмёт /start - он будет записан как ваш реферал
4. После регистрации друга вы получите прогресс к подарку
"""
    
    await callback.message.edit_text(text, reply_markup=get_free_bear_keyboard(), parse_mode="HTML")


@router.callback_query(F.data == "free_bear")
async def referral_menu(callback: CallbackQuery):
    """Открыть реферальную программу"""
    user = user_manager.get_user(callback.from_user.id)
    
    if not user:
        await callback.answer("❌ Ошибка: пользователь не найден", show_alert=True)
        return
    
    total_refs = user.get('total_referrals', 0)
    active_refs = user.get('active_referrals', 0)
    gifts_earned = user.get('gifts_earned', 0)
    bears = user.get('bears', 0)
    
    # Сколько ещё нужно пригласить для следующего подарка
    refs_needed = REFERRAL_COUNT_FOR_GIFT - (active_refs % REFERRAL_COUNT_FOR_GIFT)
    
    referral_link = f"https://t.me/testpodarkibotiksbot?start={user['referral_code']}"
    
    text = f"""
🐻 <b>РЕФЕРАЛЬНАЯ ПРОГРАММА</b>

📊 <b>Ваша статистика:</b>
👥 Всего приглашено: {total_refs} человек
✅ Активных рефералов: {active_refs}

📣 <b>Ваша реф. ссылка:</b>
<code>{referral_link}</code>

💡 <b>Как работает система:</b>
1️⃣ Скопируйте вашу ссылку
2️⃣ Пошлите её друзьям
3️⃣ Когда друг зайдёт по ссылке и зарегистрируется - получите бонус
4️⃣ За каждых {REFERRAL_COUNT_FOR_GIFT} приглашений - 1 подарок 🎁
"""
    
    await callback.message.edit_text(text, reply_markup=get_free_bear_keyboard(), parse_mode="HTML")


@router.callback_query(F.data == "withdraw_bear")
async def withdraw_bear(callback: CallbackQuery):
    """Вывести медведя"""
    user = user_manager.get_user(callback.from_user.id)
    
    if not user:
        await callback.answer("❌ Ошибка: пользователь не найден", show_alert=True)
        return
    
    active_refs = user.get('active_referrals', 0)
    bears = user.get('bears', 0)
    
    # Проверка: есть ли медведи для вывода
    if bears <= 0:
        await callback.answer(
            "❌ У вас нет медведей для вывода!\n\n"
            "Приглашайте друзей по вашей реф. ссылке и получайте подарки!",
            show_alert=True
        )
        return
    
    # Проверка: достаточно ли рефералов (минимум 5 активных)
    min_referrals_for_withdrawal = 5
    if active_refs < min_referrals_for_withdrawal:
        still_needed = min_referrals_for_withdrawal - active_refs
        await callback.answer(
            f"❌ Недостаточно активных рефералов!\n\n"
            f"✅ У вас сейчас: {active_refs} рефералов\n"
            f"⬜ Нужно еще: {still_needed} рефералов\n\n"
            f"Приглашайте еще {still_needed} человек и сможете вывести медведей!",
            show_alert=True
        )
        return
    
    # Создать запрос на вывод
    user_manager.request_withdrawal(callback.from_user.id, bears)
    
    # Обновить баланс (вычесть выводимые медведи из баланса и добавить в счётчик выводов)
    withdrawn_gifts = user.get('withdrawn_gifts', 0) + bears
    user_manager.update_user(callback.from_user.id, {
        'bears': 0,
        'withdrawn_gifts': withdrawn_gifts
    })
    
    # Отправить уведомление админам
    admin_notification = f"""
🔔 <b>НОВЫЙ ЗАПРОС НА ВЫВОД</b>

👤 <b>Пользователь:</b> {callback.from_user.first_name} (@{callback.from_user.username or 'нет username'})
🆔 <b>ID:</b> <code>{callback.from_user.id}</code>
🐻 <b>Медведей к выводу:</b> {bears}
✅ <b>Активных рефералов:</b> {user.get('active_referrals', 0)}
📅 <b>Дата:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}

⏳ <b>Статус:</b> На рассмотрении
"""
    
    # Клавиатура для админов
    admin_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Одобрить", callback_data=f"approve_withdrawal_{callback.from_user.id}"),
            InlineKeyboardButton(text="❌ Отклонить", callback_data=f"reject_withdrawal_{callback.from_user.id}")
        ]
    ])
    
    # Отправить всем админам
    try:
        for admin_id in ADMIN_IDS:
            await callback.bot.send_message(
                admin_id,
                admin_notification,
                reply_markup=admin_keyboard,
                parse_mode="HTML"
            )
    except Exception as e:
        print(f"Ошибка при отправке уведомления админам: {e}")
    
    text = f"""
✅ <b>ЗАПРОС НА ВЫВОД СОЗДАН</b>

🐻 <b>Количество медведей:</b> {bears}
👤 <b>ID:</b> {callback.from_user.id}
📅 <b>Дата:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}

⏳ Статус: <b>На рассмотрении</b>

📬 Ваш запрос был отправлен администраторам.
Ожидайте подтверждения!
"""
    
    await callback.message.edit_text(text, reply_markup=get_free_bear_keyboard(), parse_mode="HTML")
    
    await callback.answer(f"✅ Запрос на вывод {bears} медведей создан!", show_alert=True)
