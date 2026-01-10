"""
Простая версия бота для тестирования - без проверки подписки
"""

import logging
import asyncio
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import BotCommand, Message, CallbackQuery
from aiogram.filters import CommandStart
from config import BOT_TOKEN
from database.db_json import user_manager
from utils.keyboards import get_main_menu_keyboard, get_shop_keyboard, get_roulette_keyboard, get_free_bear_keyboard

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Создать роутер
router = Router()


@router.message(CommandStart())
async def start_command(message: Message):
    """Обработка команды /start"""
    user = user_manager.get_or_create_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )
    
    logger.info(f"Пользователь {message.from_user.username} ({message.from_user.id}) запустил бота")
    
    await message.answer(
        f"👋 Добро пожаловать, {message.from_user.first_name}!\n\n"
        f"💰 Ваш баланс:\n"
        f"⭐ Звёзд: {user['stars']}\n"
        f"🐻 Медведей: {user['bears']}\n\n"
        f"Выберите что вы хотите сделать:",
        reply_markup=get_main_menu_keyboard()
    )


@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery):
    """Вернуться в главное меню"""
    user = user_manager.get_user(callback.from_user.id)
    
    if not user:
        await callback.answer("❌ Ошибка: пользователь не найден", show_alert=True)
        return
    
    await callback.message.edit_text(
        f"👋 Главное меню\n\n"
        f"💰 Ваш баланс:\n"
        f"⭐ Звёзд: {user['stars']}\n"
        f"🐻 Медведей: {user['bears']}\n\n"
        f"Выберите что вы хотите сделать:",
        reply_markup=get_main_menu_keyboard()
    )


@router.callback_query(F.data == "shop")
async def shop_menu(callback: CallbackQuery):
    """Открыть магазин"""
    user = user_manager.get_user(callback.from_user.id)
    if user:
        await callback.message.edit_text(
            f"🎁 Магазин подарков\n\n💰 Баланс: {user['stars']}⭐\n\nВыберите товар:",
            reply_markup=get_shop_keyboard()
        )


@router.callback_query(F.data == "roulette")
async def roulette_menu(callback: CallbackQuery):
    """Открыть рулетку"""
    user = user_manager.get_user(callback.from_user.id)
    if user:
        await callback.message.edit_text(
            f"🎡 Рулетка\n\n💰 Баланс: {user['stars']}⭐\n\nВыберите билет:",
            reply_markup=get_roulette_keyboard()
        )


@router.callback_query(F.data == "free_bear")
async def free_bear_menu(callback: CallbackQuery):
    """Реферальная программа"""
    user = user_manager.get_user(callback.from_user.id)
    if user:
        await callback.message.edit_text(
            f"🐻 Реферальная программа\n\n"
            f"🎁 Ваша реф. ссылка: <code>https://t.me/testpodarkibotiksbot?start={user['referral_code']}</code>\n\n"
            f"Медведей: {user['bears']}",
            reply_markup=get_free_bear_keyboard()
        )


@router.callback_query(F.data == "profile")
async def profile_menu(callback: CallbackQuery):
    """Профиль"""
    user = user_manager.get_user(callback.from_user.id)
    if user:
        await callback.message.edit_text(
            f"👤 Профиль\n\n"
            f"📱 Username: @{user['username'] or 'Не указано'}\n"
            f"💰 Баланс: {user['stars']}⭐\n"
            f"🐻 Медведей: {user['bears']}\n"
            f"🔗 Реф. код: <code>{user['referral_code']}</code>",
            reply_markup=get_main_menu_keyboard()
        )


@router.callback_query(F.data.startswith("shop_item_"))
async def shop_item(callback: CallbackQuery):
    """Товар в магазине"""
    from config import SHOP_ITEMS
    item_id = int(callback.data.split("_")[2])
    item = next((i for i in SHOP_ITEMS if i['id'] == item_id), None)
    
    if item:
        user = user_manager.get_user(callback.from_user.id)
        await callback.message.edit_text(
            f"🎁 {item['name']}\n\n"
            f"📝 {item['description']}\n"
            f"💰 Цена: {item['price']}⭐\n"
            f"💵 Ваш баланс: {user['stars']}⭐\n\n"
            f"Хотите купить?",
            reply_markup=get_shop_keyboard()
        )


async def set_default_commands(bot: Bot):
    """Установить команды"""
    commands = [
        BotCommand(command="start", description="Начать работу"),
        BotCommand(command="menu", description="Главное меню"),
    ]
    await bot.set_my_commands(commands)


async def main():
    """Главная функция"""
    logger.info("🤖 Запуск бота...")
    
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    await set_default_commands(bot)
    
    dp.include_router(router)
    
    logger.info("✅ Бот запущен и ждёт команд")
    logger.info("Отправьте /start боту в Telegram")
    
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("⏹️ Бот остановлен")
