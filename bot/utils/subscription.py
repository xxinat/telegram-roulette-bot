"""
Утилиты для проверки подписки Telegram
"""

from aiogram import Bot
from aiogram.types import ChatMember
from typing import List, Dict
from config import CHANNELS_TO_SUBSCRIBE


async def check_subscription(bot: Bot, user_id: int, channels: List[Dict] = None) -> tuple:
    """
    Проверить подписку пользователя на каналы
    Возвращает: (все_подписан: bool, не_подписанные_каналы: List[Dict])
    """
    if channels is None:
        channels = CHANNELS_TO_SUBSCRIBE
    
    not_subscribed = []
    
    for channel in channels:
        try:
            member = await bot.get_chat_member(channel["channel_id"], user_id)
            
            # Проверяем статус подписки
            if member.status not in ["member", "administrator", "creator"]:
                not_subscribed.append(channel)
        except Exception as e:
            print(f"Ошибка при проверке подписки на канал {channel['name']}: {e}")
            # Если ошибка, считаем что не подписан
            not_subscribed.append(channel)
    
    is_subscribed_to_all = len(not_subscribed) == 0
    return is_subscribed_to_all, not_subscribed


async def send_subscription_check_message(bot: Bot, user_id: int, channels: List[Dict] = None) -> Dict:
    """
    Отправить сообщение о необходимости подписки
    Возвращает информацию о подписке
    """
    is_subscribed, not_subscribed = await check_subscription(bot, user_id, channels)
    
    return {
        "is_subscribed": is_subscribed,
        "not_subscribed_channels": not_subscribed,
        "channels_to_subscribe": channels or CHANNELS_TO_SUBSCRIBE
    }


def get_subscription_message_text(not_subscribed: List[Dict]) -> str:
    """Получить текст сообщения о подписке"""
    if not not_subscribed:
        return "✅ Вы подписаны на все необходимые каналы!"
    
    channels_text = "\n".join([f"• {ch['name']} ({ch['username']})" for ch in not_subscribed])
    
    return f"""
⚠️ Для продолжения работы необходимо подписаться на следующие каналы:

{channels_text}

Пожалуйста, подпишитесь на все указанные каналы и нажмите кнопку "Проверить подписку" ниже.
"""
