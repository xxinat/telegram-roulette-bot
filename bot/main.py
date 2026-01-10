"""
Главный файл Telegram бота
РЕАЛЬНАЯ ПЛАТЕЖНАЯ СИСТЕМА - Telegram Stars и Подарки
"""

import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from config import BOT_TOKEN
from database.db_json import db  # JSON вместо SQLAlchemy
from handlers import start, menu, shop, roulette, referral, payments, admin

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def set_default_commands(bot: Bot):
    """Установить команды по умолчанию"""
    commands = [
        BotCommand(command="start", description="Начать работу и получить реф. ссылку"),
        BotCommand(command="menu", description="Главное меню"),
    ]
    await bot.set_my_commands(commands)


async def main():
    """Главная функция"""
    logger.info("📦 Инициализация JSON базы данных...")
    logger.info("✅ JSON база данных готова")
    
    # Создать бота и диспетчер
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    # Установить команды
    await set_default_commands(bot)
    
    # Подключить обработчики
    dp.include_router(start.router)
    dp.include_router(menu.router)
    dp.include_router(shop.router)
    dp.include_router(roulette.router)  # Рулетка с Invoice
    dp.include_router(referral.router)  # Реферальная система
    dp.include_router(payments.router)  # Обработчик платежей Telegram Stars
    dp.include_router(admin.router)  # Админ панель
    
    logger.info("🤖 Бот запущен! Используется Telegram Stars и подарки")
    
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("⏹️ Бот остановлен пользователем")
