"""
Магазин Telegram подарков - платёж в Telegram Stars Invoice
"""

from aiogram import Router, F
from aiogram.types import CallbackQuery, LabeledPrice
from database.db_json import user_manager, purchase_manager
from utils.keyboards import get_shop_item_keyboard, get_main_menu_keyboard, get_shop_keyboard
from config import SHOP_ITEMS

router = Router()


def get_item_by_id(item_id: int):
    """Получить товар по ID"""
    for item in SHOP_ITEMS:
        if item["id"] == item_id:
            return item
    return None


@router.callback_query(F.data.startswith("shop_item_"))
async def shop_item_detail(callback: CallbackQuery):
    """Показать детали товара Telegram"""
    try:
        item_id = int(callback.data.split("_")[2])
        item = get_item_by_id(item_id)
        
        if not item:
            await callback.answer("❌ Товар не найден", show_alert=True)
            return
        
        user = user_manager.get_user(callback.from_user.id)
        
        text = f"""
🎁 <b>{item['name']}</b>

📝 <b>Описание:</b> {item['description']}
⭐ <b>Цена:</b> {item['price']} Telegram Stars
"""
        
        await callback.message.edit_text(text, reply_markup=get_shop_item_keyboard(item_id), parse_mode="HTML")
    except Exception as e:
        await callback.answer(f"❌ Ошибка: {str(e)}", show_alert=True)


@router.callback_query(F.data.startswith("buy_item_"))
async def buy_item(callback: CallbackQuery):
    """Купить товар - отправить счёт на оплату"""
    try:
        item_id = int(callback.data.split("_")[2])
        item = get_item_by_id(item_id)
        
        if not item:
            await callback.answer("❌ Товар не найден", show_alert=True)
            return
        
        # Создать счёт для оплаты в Telegram Stars
        prices = [LabeledPrice(
            label=item['name'],
            amount=item['price']
        )]
        
        await callback.bot.send_invoice(
            chat_id=callback.from_user.id,
            title=f"🎁 {item['name']}",
            description=item.get('description', 'Подарок из магазина'),
            payload=f"shop_item_{item_id}",
            provider_token="",
            currency="XTR",
            prices=prices
        )
        
        await callback.answer("✅ Счёт отправлен!", show_alert=False)
    
    except Exception as e:
        await callback.answer(f"❌ Ошибка: {str(e)}", show_alert=True)


@router.callback_query(F.data == "shop_back")
async def shop_back(callback: CallbackQuery):
    """Вернуться в меню магазина"""
    try:
        user = user_manager.get_user(callback.from_user.id)
        
        if not user:
            await callback.answer("❌ Ошибка: пользователь не найден", show_alert=True)
            return
        
        await callback.message.edit_text(
            f"🎁 <b>Магазин подарков Telegram</b>\n\n"
            f"Здесь вы можете купить подарки за Telegram Stars\n\n"
            f"Выберите подарок для покупки:",
            reply_markup=get_shop_keyboard(),
            parse_mode="HTML"
        )
    except Exception as e:
        await callback.answer(f"❌ Ошибка: {str(e)}", show_alert=True)
