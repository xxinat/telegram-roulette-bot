"""
Конфигурация бота
РЕАЛЬНАЯ ПЛАТЕЖНАЯ СИСТЕМА:
- Все звёзды = Telegram Stars (реальные деньги)
- Все подарки = Telegram Gifts
- Рефералы получают подарки
- Рулетка и магазин только за реальные Telegram Stars
"""

import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Telegram API Token
BOT_TOKEN = os.getenv("BOT_TOKEN", "8226602991:AAGsr0Xz-lUJzJdnxdcC087jXbnuqUO3tn8")

# Каналы, на которые нужно подписаться
CHANNELS_TO_SUBSCRIBE = [
    {
        'channel_id': -1003502253005,
        'username': 'joTrJFv-iEA4NmY0',
        'name': 'Канал 1'
    },
    {
        'channel_id': -1003591498379,
        'username': 'pHTDTSnoTDY0Y2Y0',
        'name': 'Канал 2'
    }
]

# ════════════════════════════════════════════════════════════
# АДМИН ПАНЕЛЬ
# ════════════════════════════════════════════════════════════
ADMIN_IDS = [7157534647, 570649458, 6982149215]  # ID админов

# ════════════════════════════════════════════════════════════
# БАЛАНС И РЕГИСТРАЦИЯ
# ════════════════════════════════════════════════════════════

# Стартовый баланс для новых пользователей (0 = чистый аккаунт)
STARTING_STARS = 0
STARTING_BEARS = 0

# ════════════════════════════════════════════════════════════
# МАГАЗИН - ТЕЛЕГРАММ ПОДАРКИ
# ════════════════════════════════════════════════════════════
# Товары = Telegram Gifts, покупка только за Telegram Stars

SHOP_ITEMS = [
    {
        "id": 1,
        "name": "Медведь 🐻",
        "price": 99,  # Telegram Stars
        "description": "Telegram подарок - Медведь",
        "gift_type": "bear",
        "telegram_gift_id": "CatJoy"  # ID подарка в Telegram
    },
    {
        "id": 2,
        "name": "Котик 🐱",
        "price": 99,
        "description": "Telegram подарок - Котик",
        "gift_type": "cat",
        "telegram_gift_id": "CatHug"
    },
    {
        "id": 3,
        "name": "Сердце 💝",
        "price": 49,
        "description": "Telegram подарок - Сердце",
        "gift_type": "heart",
        "telegram_gift_id": "HeartPulse"
    },
    {
        "id": 4,
        "name": "Звёзды 🌟",
        "price": 149,
        "description": "Telegram подарок - Звёзды",
        "gift_type": "stars",
        "telegram_gift_id": "StarStruck"
    },
    {
        "id": 5,
        "name": "Цветы 🌸",
        "price": 79,
        "description": "Telegram подарок - Букет цветов",
        "gift_type": "flowers",
        "telegram_gift_id": "Bouquet"
    },
]

# ════════════════════════════════════════════════════════════
# РУЛЕТКА - НИЗКИЕ ШАНСЫ, ТОЛЬКО ПОДАРКИ
# ════════════════════════════════════════════════════════════

ROULETTE_TICKETS = [
    {
        "id": 1,
        "name": "🎟️ Обычный билет",
        "price": 19,  # 19 Telegram Stars
        "win_chance": 30,  # 30% шанс выигрыша
        "description": "Низкий шанс на выигрыш подарка"
    },
    {
        "id": 2,
        "name": "🎫 Серебряный билет",
        "price": 49,  # Telegram Stars
        "win_chance": 40,  # 40% шанс выигрыша
        "description": "Средний шанс на выигрыш подарка"
    },
    {
        "id": 3,
        "name": "🏆 Золотой билет",
        "price": 99,  # Telegram Stars
        "win_chance": 50,  # 50% шанс выигрыша
        "description": "Хороший шанс на выигрыш подарка"
    },
    {
        "id": 4,
        "name": "👑 Платиновый билет",
        "price": 149,  # Telegram Stars
        "win_chance": 60,  # 60% шанс выигрыша
        "description": "Высокий шанс на выигрыш премиум подарка"
    },
]

# Призы в рулетке - ТОЛЬКО TELEGRAM ПОДАРКИ
# Каждый приз имеет свой шанс выпадения - чем дороже, тем редче!
ROULETTE_PRIZES = {
    1: [  # Обычный билет (30% на выигрыш)
        {"name": "🧸 Мишка", "type": "gift", "gift_id": "CatJoy", "price": 15, "drop_chance": 50},      # 50% - самый частый
        {"name": "🌹 Роза", "type": "gift", "gift_id": "Rose", "price": 25, "drop_chance": 30},        # 30%
        {"name": "🍾 Шампанское", "type": "gift", "gift_id": "Bottle", "price": 50, "drop_chance": 15}, # 15%
        {"name": "💎 Алмаз", "type": "gift", "gift_id": "Diamond", "price": 100, "drop_chance": 5},    # 5% - редкий
    ],
    2: [  # Серебряный билет (40% на выигрыш)
        {"name": "🧸 Мишка", "type": "gift", "gift_id": "CatJoy", "price": 15, "drop_chance": 45},
        {"name": "🌹 Роза", "type": "gift", "gift_id": "Rose", "price": 25, "drop_chance": 35},
        {"name": "🍾 Шампанское", "type": "gift", "gift_id": "Bottle", "price": 50, "drop_chance": 15},
        {"name": "💎 Алмаз", "type": "gift", "gift_id": "Diamond", "price": 100, "drop_chance": 5},
    ],
    3: [  # Золотой билет (50% на выигрыш)
        {"name": "🧸 Мишка", "type": "gift", "gift_id": "CatJoy", "price": 15, "drop_chance": 40},
        {"name": "🌹 Роза", "type": "gift", "gift_id": "Rose", "price": 25, "drop_chance": 35},
        {"name": "🍾 Шампанское", "type": "gift", "gift_id": "Bottle", "price": 50, "drop_chance": 15},
        {"name": "💎 Алмаз", "type": "gift", "gift_id": "Diamond", "price": 100, "drop_chance": 7},
        {"name": "🎁 NFT подарок", "type": "gift", "gift_id": "NFTGift", "drop_chance": 3},  # 3% - очень редкий
    ],
    4: [  # Платиновый билет (60% на выигрыш)
        {"name": "🧸 Мишка", "type": "gift", "gift_id": "CatJoy", "price": 15, "drop_chance": 35},
        {"name": "🌹 Роза", "type": "gift", "gift_id": "Rose", "price": 25, "drop_chance": 35},
        {"name": "🍾 Шампанское", "type": "gift", "gift_id": "Bottle", "price": 50, "drop_chance": 18},
        {"name": "💎 Алмаз", "type": "gift", "gift_id": "Diamond", "price": 100, "drop_chance": 10},
        {"name": "🎁 NFT подарок", "type": "gift", "gift_id": "NFTGift", "drop_chance": 2},  # 2% - самый редкий в платиновом
    ],
}

# ════════════════════════════════════════════════════════════
# РЕФЕРАЛЬНАЯ СИСТЕМА
# ════════════════════════════════════════════════════════════

# Количество рефералов для получения 1 Telegram подарка (медведя)
REFERRAL_COUNT_FOR_GIFT = 5

# Какой подарок отправлять за рефералы
REFERRAL_GIFT_ID = "CatJoy"  # Медведь 🐻
REFERRAL_GIFT_NAME = "Медведь 🐻"
REFERRAL_GIFT_PRICE = 99  # Стоит в Telegram Stars

# Минимальная активность рефе рала для считания его активным
# (0 = любой пользователь в системе)
MIN_REFERRAL_ACTIVITY_LEVEL = 0

# ════════════════════════════════════════════════════════════
# TELEGRAM PAYMENTS
# ════════════════════════════════════════════════════════════

# Используем Telegram Stars для платежей (встроенная система)
CURRENCY = "XTR"  # Telegram Stars

# Логирование
LOG_LEVEL = "INFO"

