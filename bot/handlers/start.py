"""
Обработчик команды /start и проверки подписки
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from database.db_json import user_manager
from utils.subscription import check_subscription, get_subscription_message_text
from utils.keyboards import get_subscription_keyboard, get_main_menu_keyboard
from config import CHANNELS_TO_SUBSCRIBE

router = Router()


@router.message(CommandStart())
async def start_command(message: Message):
    """Обработка команды /start"""
    # Получить аргументы (/start ref_code)
    args = message.text.split()
    referral_code = args[1] if len(args) > 1 else None
    
    user = user_manager.get_or_create_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )
    
    # Обработать реф. код если это новый пользователь
    if referral_code and user.get('referred_by') is None:
        from database.db_json import referral_manager
        referrer = referral_manager.get_user_by_referral_code(referral_code)
        
        if referrer and referrer['telegram_id'] != message.from_user.id:
            # Записать что этого пользователя пригласил другой
            referral_manager.add_referral(
                referrer_id=referrer['telegram_id'],
                referred_user_id=message.from_user.id,
                referred_username=message.from_user.username
            )
            
            # Обновить статистику реферера
            user_manager.update_user(referrer['telegram_id'], {
                'total_referrals': referrer.get('total_referrals', 0) + 1,
                'active_referrals': referrer.get('active_referrals', 0) + 1
            })
            
            # Отметить что пользователь приглашён
            user_manager.update_user(message.from_user.id, {
                'referred_by': referrer['telegram_id']
            })
            
            await message.answer(
                f"✅ Спасибо что зарегистрировались по реф. ссылке!\n\n"
                f"Реферер получит бонус за ваше приглашение 🎁"
            )
    
    # Если каналов нет, сразу показать меню
    if not CHANNELS_TO_SUBSCRIBE:
        await message.answer(
            f"👋 Добро пожаловать, {message.from_user.first_name}!\n\n"
            f"💡 Как зарабатывать подарки?\n"
            f"Приглашайте друзей и получайте подарки! 🎉\n\n"
            f"Выберите действие:",
            reply_markup=get_main_menu_keyboard(),
            parse_mode="HTML"
        )
        return
    
    # Проверить подписку
    is_subscribed, not_subscribed = await check_subscription(message.bot, message.from_user.id)
    
    if is_subscribed and user.get('subscription_verified', False):
        # Пользователь уже подписан
        await message.answer(
            f"👋 Добро пожаловать, {message.from_user.first_name}!\n\n"
            f"Выберите что вы хотите сделать:",
            reply_markup=get_main_menu_keyboard(),
            parse_mode="HTML"
        )
    else:
        # Нужно подписаться на каналы
        text = get_subscription_message_text(CHANNELS_TO_SUBSCRIBE)
        await message.answer(
            text,
            reply_markup=get_subscription_keyboard(CHANNELS_TO_SUBSCRIBE)
        )


@router.callback_query(F.data == "check_subscription")
async def check_subscription_callback(callback: CallbackQuery):
    """Обработка нажатия кнопки 'Проверить подписку'"""
    user = user_manager.get_user(callback.from_user.id)
    
    is_subscribed, not_subscribed = await check_subscription(callback.bot, callback.from_user.id)
    
    if is_subscribed:
        # Пользователь подписан на все каналы
        user_manager.verify_subscription(callback.from_user.id)
        
        await callback.answer("✅ Спасибо за подписку!", show_alert=True)
        
        await callback.message.edit_text(
            f"👋 Добро пожаловать, {callback.from_user.first_name}!\n\n"
            f"Выберите что вы хотите сделать:",
            reply_markup=get_main_menu_keyboard(),
            parse_mode="HTML"
        )
    else:
        # Пользователь не подписан на все каналы
        text = get_subscription_message_text(CHANNELS_TO_SUBSCRIBE)
        
        await callback.answer(f"❌ Вы еще не подписаны на все каналы", show_alert=True)
        
        await callback.message.edit_text(
            text,
            reply_markup=get_subscription_keyboard(CHANNELS_TO_SUBSCRIBE)
        )
