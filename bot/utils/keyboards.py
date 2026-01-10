"""
Клавиатуры для бота
"""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from config import SHOP_ITEMS, ROULETTE_TICKETS
from typing import List, Dict


def get_subscription_keyboard(channels: List[Dict] = None) -> InlineKeyboardMarkup:
    """Клавиатура для подписки на каналы с кнопками ссылок"""
    from config import CHANNELS_TO_SUBSCRIBE
    
    buttons = []
    channels_list = channels or CHANNELS_TO_SUBSCRIBE
    
    # Добавляем кнопки для каждого канала
    for channel in channels_list:
        text = f"📢 {channel['name']}"
        # Используем username для приватного канала
        url = f"https://t.me/+{channel['username']}"
        buttons.append([InlineKeyboardButton(text=text, url=url)])
    
    # Добавляем кнопку проверки подписки в конец
    buttons.append([InlineKeyboardButton(text="✅ Проверить подписку", callback_data="check_subscription")])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """Главное меню"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎁 Магазин подарков", callback_data="shop")],
        [InlineKeyboardButton(text="🎡 Рулетка", callback_data="roulette")],
        [InlineKeyboardButton(text="🐻 Бесплатный мишка", callback_data="free_bear")],
        [InlineKeyboardButton(text="👤 Мой профиль", callback_data="profile")],
    ])
    return keyboard


def get_shop_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура магазина"""
    buttons = []
    
    for item in SHOP_ITEMS:
        text = f"{item['name']} - {item['price']}⭐"
        callback = f"shop_item_{item['id']}"
        buttons.append([InlineKeyboardButton(text=text, callback_data=callback)])
    
    buttons.append([InlineKeyboardButton(text="← Назад", callback_data="back_to_menu")])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_shop_item_keyboard(item_id: int) -> InlineKeyboardMarkup:
    """Клавиатура для выбора товара"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Купить", callback_data=f"buy_item_{item_id}")],
        [InlineKeyboardButton(text="← Назад в магазин", callback_data="shop")],
    ])
    return keyboard


def get_roulette_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура рулетки"""
    buttons = []
    
    for ticket in ROULETTE_TICKETS:
        text = f"{ticket['name']} - {ticket['price']}⭐"
        callback = f"roulette_ticket_{ticket['id']}"
        buttons.append([InlineKeyboardButton(text=text, callback_data=callback)])
    
    buttons.append([InlineKeyboardButton(text="← Назад", callback_data="back_to_menu")])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_roulette_ticket_keyboard(ticket_id: int) -> InlineKeyboardMarkup:
    """Клавиатура для подтверждения покупки билета рулетки"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎰 Купить билет и сыграть", callback_data=f"buy_ticket_{ticket_id}")],
        [InlineKeyboardButton(text="← Назад к билетам", callback_data="roulette")],
    ])
    return keyboard


def get_free_bear_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура реферальной программы"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📋 Моя реф. ссылка", callback_data="my_referral_link")],
        [InlineKeyboardButton(text="👥 Мои приглашения", callback_data="my_referrals")],
        [InlineKeyboardButton(text="💸 Вывести медведя", callback_data="withdraw_bear")],
        [InlineKeyboardButton(text="← Назад", callback_data="back_to_menu")],
    ])
    return keyboard


def get_back_menu_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура возврата в меню"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="← Назад в меню", callback_data="back_to_menu")]
    ])
    return keyboard


def get_confirm_keyboard(action: str, item_id: int = None) -> InlineKeyboardMarkup:
    """Клавиатура подтверждения"""
    if item_id:
        yes_callback = f"confirm_{action}_{item_id}"
    else:
        yes_callback = f"confirm_{action}"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Да", callback_data=yes_callback),
         InlineKeyboardButton(text="❌ Нет", callback_data="back_to_menu")],
    ])
    return keyboard
