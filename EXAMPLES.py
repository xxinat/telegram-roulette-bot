"""
Примеры расширенной конфигурации для разных сценариев
"""

# ==================== ПРИМЕР 1: МИНИМАЛЬНАЯ КОНФИГУРАЦИЯ ====================
# Для тестирования без проверки подписки на каналы

MINIMAL_CONFIG = {
    "BOT_TOKEN": "YOUR_BOT_TOKEN",
    "CHANNELS_TO_SUBSCRIBE": [],  # Пусто = нет проверки подписки
    "STARTING_STARS": 50,
}

# ==================== ПРИМЕР 2: РАСШИРЕННАЯ КОНФИГУРАЦИЯ ====================
# С дополнительными товарами и билетами

EXTENDED_SHOP = [
    {"id": 1, "name": "Кофе ☕", "price": 5, "description": "Горячий кофе"},
    {"id": 2, "name": "Чай 🍵", "price": 8, "description": "Ароматный чай"},
    {"id": 3, "name": "Пицца 🍕", "price": 25, "description": "Вкусная пицца"},
    {"id": 4, "name": "Бургер 🍔", "price": 20, "description": "Сочный бургер"},
    {"id": 5, "name": "Салат 🥗", "price": 15, "description": "Свежий салат"},
    {"id": 6, "name": "Макароны 🍝", "price": 12, "description": "Паста аль денте"},
    {"id": 7, "name": "Рис 🍚", "price": 10, "description": "Рассыпчатый рис"},
    {"id": 8, "name": "Суп 🍲", "price": 18, "description": "Горячий суп"},
    {"id": 9, "name": "Наггетсы 🍟", "price": 14, "description": "Хрустящие наггетсы"},
    {"id": 10, "name": "Молоко 🥛", "price": 6, "description": "Свежее молоко"},
]

EXTENDED_ROULETTE = [
    {"id": 1, "name": "Компромиссный билет", "price": 5, "rarity": 1},
    {"id": 2, "name": "Обычный билет", "price": 10, "rarity": 1},
    {"id": 3, "name": "Улучшенный билет", "price": 25, "rarity": 1},
    {"id": 4, "name": "Серебряный билет", "price": 50, "rarity": 2},
    {"id": 5, "name": "Золотой билет", "price": 100, "rarity": 3},
    {"id": 6, "name": "Платиновый билет", "price": 200, "rarity": 5},
    {"id": 7, "name": "Алмазный билет", "price": 500, "rarity": 10},
]

# ==================== ПРИМЕР 3: МНОГО КАНАЛОВ ====================

MULTI_CHANNEL_CONFIG = [
    {
        "name": "Новости 📰",
        "username": "@news_channel",
        "chat_id": -1001111111111
    },
    {
        "name": "Развлечения 🎬",
        "username": "@entertainment",
        "chat_id": -1001222222222
    },
    {
        "name": "Техника 🔧",
        "username": "@tech_news",
        "chat_id": -1001333333333
    },
    {
        "name": "Бизнес 💼",
        "username": "@business_channel",
        "chat_id": -1001444444444
    },
]

# ==================== ПРИМЕР 4: СПЕЦИАЛЬНЫЕ ПРИЗЫ ====================

SPECIAL_PRIZES = {
    1: [
        {"name": "1 звезда ⭐", "type": "stars", "value": 1, "probability": 25},
        {"name": "5 звёзд ⭐⭐", "type": "stars", "value": 5, "probability": 40},
        {"name": "Ничего 😭", "type": "nothing", "value": 0, "probability": 35},
    ],
    2: [
        {"name": "10 звёзд ⭐", "type": "stars", "value": 10, "probability": 30},
        {"name": "25 звёзд ⭐⭐", "type": "stars", "value": 25, "probability": 35},
        {"name": "3 медведя 🐻", "type": "bears", "value": 3, "probability": 25},
        {"name": "Ничего 😢", "type": "nothing", "value": 0, "probability": 10},
    ],
    3: [
        {"name": "50 звёзд ⭐", "type": "stars", "value": 50, "probability": 25},
        {"name": "100 звёзд ⭐⭐", "type": "stars", "value": 100, "probability": 25},
        {"name": "10 медведей 🐻", "type": "bears", "value": 10, "probability": 30},
        {"name": "VIP статус", "type": "vip", "value": 1, "probability": 10},
        {"name": "Ничего 😢", "type": "nothing", "value": 0, "probability": 10},
    ],
    5: [
        {"name": "500 звёзд ⭐⭐⭐", "type": "stars", "value": 500, "probability": 15},
        {"name": "1000 звёзд ⭐⭐⭐⭐", "type": "stars", "value": 1000, "probability": 15},
        {"name": "100 медведей 🐻🐻", "type": "bears", "value": 100, "probability": 20},
        {"name": "Премиум подарок 🎁", "type": "premium", "value": 1, "probability": 20},
        {"name": "Суперприз 🏆", "type": "super_prize", "value": 1, "probability": 20},
        {"name": "Легендарный предмет ⚔️", "type": "legendary", "value": 1, "probability": 10},
    ],
    10: [
        {"name": "10000 звёзд 💰💰💰", "type": "stars", "value": 10000, "probability": 10},
        {"name": "1000 медведей 🐻🐻🐻", "type": "bears", "value": 1000, "probability": 10},
        {"name": "Статус Легенды", "type": "legend_status", "value": 1, "probability": 20},
        {"name": "Айфон 13 📱", "type": "phone", "value": 1, "probability": 10},
        {"name": "Макбук 💻", "type": "laptop", "value": 1, "probability": 10},
        {"name": "Золото 🪙", "type": "gold", "value": 1000, "probability": 20},
        {"name": "Квартира 🏠", "type": "apartment", "value": 1, "probability": 5},
        {"name": "Автомобиль 🚗", "type": "car", "value": 1, "probability": 5},
        {"name": "Путешествие 🌍", "type": "trip", "value": 1, "probability": 10},
    ],
}

# ==================== ПРИМЕР 5: ПРОГРЕССИВНЫЕ НАГРАДЫ ====================

PROGRESSIVE_REWARDS = {
    "invites": {
        5: {"bears": 1, "stars": 50},
        10: {"bears": 2, "stars": 100},
        25: {"bears": 5, "stars": 250},
        50: {"bears": 10, "stars": 500},
        100: {"bears": 20, "stars": 1000, "vip": True},
    }
}

# ==================== ПРИМЕР 6: СЕЗОННЫЕ ПРЕДЛОЖЕНИЯ ====================

SEASONAL_DISCOUNTS = {
    "winter": {
        "shop_discount": 0.2,  # 20% скидка
        "roulette_bonus": 1.5,  # В 1.5 раза больше звёзд
    },
    "summer": {
        "shop_discount": 0.1,  # 10% скидка
        "roulette_bonus": 1.2,  # В 1.2 раза больше звёзд
    },
}

# ==================== ПРИМЕР 7: ОГРАНИЧЕНИЯ И ЛИМИТЫ ====================

LIMITS = {
    "max_purchases_per_day": 10,
    "max_roulette_plays_per_day": 5,
    "max_referral_bonus_per_day": 20,
    "min_referral_age_hours": 24,  # Минимум 24 часа в боте
    "daily_login_bonus": 5,  # 5 звёзд за ежедневный вход
}

# ==================== ПРИМЕР 8: УРОВНЕВАЯ СИСТЕМА ====================

USER_LEVELS = {
    1: {"name": "Новичок", "min_purchases": 0, "bonus_multiplier": 1.0},
    2: {"name": "Эксперт", "min_purchases": 10, "bonus_multiplier": 1.1},
    3: {"name": "Мастер", "min_purchases": 50, "bonus_multiplier": 1.2},
    4: {"name": "Легенда", "min_purchases": 100, "bonus_multiplier": 1.5},
    5: {"name": "Боженство", "min_purchases": 500, "bonus_multiplier": 2.0},
}

# ==================== ПРИМЕР 9: АДМИН НАСТРОЙКИ ====================

ADMIN_CONFIG = {
    "admin_ids": [123456789],  # Telegram ID админов
    "log_channel_id": -1001234567890,  # Канал для логов
    "enable_admin_panel": True,
    "admin_commands": [
        "/broadcast",  # Отправить сообщение всем
        "/stats",      # Получить статистику
        "/add_stars",  # Добавить звёзды пользователю
        "/ban",        # Забанить пользователя
    ]
}

# ==================== ПРИМЕР 10: ВЕБ-ИНТЕГРАЦИЯ ====================

WEBHOOK_CONFIG = {
    "enabled": False,
    "webhook_url": "https://your-domain.com/webhook",
    "port": 8443,
    "ssl_cert": "/path/to/cert.pem",
}

# ==================== ПРИМЕР 11: АНАЛИТИКА ====================

ANALYTICS = {
    "track_user_behavior": True,
    "track_purchases": True,
    "track_referrals": True,
    "analytics_db": "analytics.db",
    "export_stats_daily": True,
}

# ==================== ПРИМЕР 12: ЛОКАЛИЗАЦИЯ ====================

LANGUAGES = {
    "ru": {
        "welcome": "👋 Добро пожаловать!",
        "shop": "🎁 Магазин",
        "roulette": "🎡 Рулетка",
    },
    "en": {
        "welcome": "👋 Welcome!",
        "shop": "🎁 Shop",
        "roulette": "🎡 Roulette",
    },
}
