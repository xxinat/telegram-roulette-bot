"""
Обработчик платежей - Telegram Stars Invoice
"""

from aiogram import Router, F
from aiogram.types import PreCheckoutQuery, Message, SuccessfulPayment
from aiogram.filters import Command
from database.db_json import user_manager, purchase_manager
from config import BOT_TOKEN, SHOP_ITEMS, ROULETTE_TICKETS, ROULETTE_PRIZES
import random

router = Router()


def get_shop_item_by_id(item_id: int):
    """Получить товар из магазина по ID"""
    for item in SHOP_ITEMS:
        if item["id"] == item_id:
            return item
    return None


def get_roulette_ticket_by_id(ticket_id: int):
    """Получить билет рулетки по ID"""
    for ticket in ROULETTE_TICKETS:
        if ticket["id"] == ticket_id:
            return ticket
    return None


def select_prize_by_chance(prizes: list):
    """
    Выбрать приз по шансам выпадения (drop_chance).
    Чем выше drop_chance, тем чаще выпадает приз.
    """
    if not prizes:
        return None
    
    total_chance = sum(p.get('drop_chance', 0) for p in prizes)
    if total_chance == 0:
        return random.choice(prizes)
    
    rand = random.randint(1, total_chance)
    current = 0
    
    for prize in prizes:
        current += prize.get('drop_chance', 0)
        if rand <= current:
            return prize
    
    return prizes[-1]  # Fallback


@router.pre_checkout_query()
async def pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    """Проверка перед платежом"""
    # Подтверждаем готовность принять платёж
    await pre_checkout_query.answer(ok=True)


@router.message(F.successful_payment)
async def successful_payment(message: Message):
    """Обработка успешного платежа"""
    payment: SuccessfulPayment = message.successful_payment
    
    user = user_manager.get_user(message.from_user.id)
    
    # payment.invoice_payload содержит информацию о товаре
    # Формат: "type:shop_item_1" или "type:roulette_ticket_2"
    payload_parts = payment.invoice_payload.split(":")
    item_type = payload_parts[0]
    item_id = int(payload_parts[1].split("_")[1])
    
    if item_type == "shop_item":
        # Товар из магазина
        item = get_shop_item_by_id(item_id)
        
        if item:
            # Добавить товар в историю
            purchase_manager.add_purchase(
                telegram_id=message.from_user.id,
                item_id=item_id,
                item_name=item['name'],
                price=item['price'],
                purchase_type="shop"
            )
            
            # Отправить подтверждение
            await message.answer(
                f"✅ <b>Покупка успешна!</b>\n\n"
                f"🎁 Вы купили: <b>{item['name']}</b>\n"
                f"⭐ Потрачено: {item['price']} Telegram Stars\n\n"
                f"<i>Подарок отправлен в ваши подарки Telegram</i>\n"
                f"<i>ID платежа: {payment.telegram_payment_charge_id}</i>"
            )
    
    elif item_type == "roulette_ticket":
        # Билет рулетки
        ticket = get_roulette_ticket_by_id(item_id)
        
        if ticket:
            import random
            
            # Добавить в историю
            purchase_manager.add_purchase(
                telegram_id=message.from_user.id,
                item_id=item_id,
                item_name=ticket['name'],
                price=ticket['price'],
                purchase_type="roulette"
            )
            
            # Крутить рулетку - двухуровневая система вероятности
            win_chance = ticket.get('win_chance', 50)
            rand = random.randint(1, 100)
            
            user = user_manager.get_user(message.from_user.id)
            
            if rand <= win_chance:
                # Выигрыш! Второй уровень: выбираем приз по шансам выпадения
                prizes = ROULETTE_PRIZES.get(item_id, [])
                if prizes:
                    prize = select_prize_by_chance(prizes)
                    
                    # Сохраняем результат в БД
                    from database.db_json import roulette_manager
                    roulette_manager.add_roulette_result(
                        telegram_id=message.from_user.id,
                        ticket_id=item_id,
                        ticket_name=ticket['name'],
                        ticket_price=ticket['price'],
                        prize_name=prize['name'],
                        prize_type=prize.get('type', 'gift'),
                        prize_value=prize.get('price', 0)
                    )
                    
                    await message.answer(
                        f"🎡 <b>РЕЗУЛЬТАТ РУЛЕТКИ!</b>\n\n"
                        f"🎟️ Билет: {ticket['name']}\n"
                        f"⭐ Потрачено: {ticket['price']} Telegram Stars\n\n"
                        f"🎉 <b>ВЫИГРАЛ!</b>\n"
                        f"🎁 Вы выиграли: <b>{prize['name']}</b>\n\n"
                        f"<i>ID платежа: {payment.telegram_payment_charge_id}</i>"
                    )
            else:
                # Проигрыш - тоже сохраняем
                from database.db_json import roulette_manager
                roulette_manager.add_roulette_result(
                    telegram_id=message.from_user.id,
                    ticket_id=item_id,
                    ticket_name=ticket['name'],
                    ticket_price=ticket['price'],
                    prize_name="❌ Ничего",
                    prize_type="no_prize",
                    prize_value=0
                )
                await message.answer(
                    f"🎡 <b>РЕЗУЛЬТАТ РУЛЕТКИ</b>\n\n"
                    f"😢 К сожалению, вы не выиграли в этот раз\n\n"
                    f"🎟️ Билет: {ticket['name']}\n"
                    f"⭐ Потрачено: {ticket['price']} Telegram Stars\n\n"
                    f"<i>Попробуйте ещё раз! ID платежа: {payment.telegram_payment_charge_id}</i>"
                )
