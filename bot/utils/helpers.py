"""
Вспомогательные утилиты
"""

from datetime import datetime
from typing import Optional
import hashlib
import uuid


def generate_unique_code(prefix: str = "REF") -> str:
    """Генерировать уникальный код"""
    unique_id = str(uuid.uuid4())[:8].upper()
    return f"{prefix}_{unique_id}"


def format_date(date: datetime) -> str:
    """Форматировать дату"""
    return date.strftime("%d.%m.%Y %H:%M")


def format_balance(stars: int, bears: int) -> str:
    """Форматировать баланс для отображения"""
    return f"⭐ {stars} | 🐻 {bears}"


def calculate_next_bear(current_invites: int, per_bear: int = 5) -> tuple:
    """
    Рассчитать прогресс медведя
    Возвращает (earned_bears, remaining_invites)
    """
    earned = current_invites // per_bear
    remaining = per_bear - (current_invites % per_bear)
    return earned, remaining


def get_rarity_emoji(rarity: int) -> str:
    """Получить emoji редкости"""
    if rarity <= 1:
        return "⭐"
    elif rarity <= 2:
        return "⭐⭐"
    elif rarity <= 3:
        return "⭐⭐⭐"
    elif rarity <= 5:
        return "⭐⭐⭐⭐"
    else:
        return "⭐⭐⭐⭐⭐"


def get_greeting_message(user_name: str, hour: Optional[int] = None) -> str:
    """Получить приветственное сообщение в зависимости от времени"""
    if hour is None:
        hour = datetime.now().hour
    
    if 5 <= hour < 12:
        greeting = "🌅 Доброе утро"
    elif 12 <= hour < 17:
        greeting = "☀️ Добрый день"
    elif 17 <= hour < 21:
        greeting = "🌆 Добрый вечер"
    else:
        greeting = "🌙 Доброй ночи"
    
    return f"{greeting}, {user_name}!"


# Текстовые шаблоны
TEMPLATES = {
    "insufficient_funds": "❌ Недостаточно звёзд. Не хватает {needed}⭐",
    "purchase_success": "✅ Вы успешно купили {item}!\n💸 Израсходовано: {price}⭐",
    "error": "❌ Произошла ошибка: {error}",
    "not_found": "❌ {what} не найдено",
}


def get_template(template_name: str, **kwargs) -> str:
    """Получить текстовый шаблон"""
    template = TEMPLATES.get(template_name, "Ошибка: шаблон не найден")
    return template.format(**kwargs)
