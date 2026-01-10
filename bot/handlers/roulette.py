"""
Обработчик рулетки - с Telegram Stars Invoice
"""

import random
from aiogram import Router, F
from aiogram.types import CallbackQuery, LabeledPrice
from database.db_json import user_manager, roulette_manager
from utils.keyboards import get_roulette_ticket_keyboard, get_roulette_keyboard, get_main_menu_keyboard
from config import ROULETTE_TICKETS, ROULETTE_PRIZES, SHOP_ITEMS

router = Router()


def get_ticket_by_id(ticket_id: int):
    """Получить билет по ID"""
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


async def spin_roulette(user_id: int, ticket_id: int):
    """Раскрутить рулетку и получить приз"""
    ticket = get_ticket_by_id(ticket_id)
    if not ticket:
        return None
    
    # Первый уровень: проверка общего шанса выигрыша
    win_chance = ticket.get('win_chance', 50)
    rand = random.randint(1, 100)
    
    if rand <= win_chance:
        # Выигрыш! Второй уровень: выбрать конкретный приз по шансам
        prizes = ROULETTE_PRIZES.get(ticket_id, [])
        if prizes:
            prize = select_prize_by_chance(prizes)
            return prize
    
    return None


@router.callback_query(F.data.startswith("roulette_ticket_"))
async def roulette_ticket_detail(callback: CallbackQuery):
    """Показать детали билета рулетки"""
    try:
        ticket_id = int(callback.data.split("_")[2])
        ticket = get_ticket_by_id(ticket_id)
        
        if not ticket:
            await callback.answer("❌ Билет не найден", show_alert=True)
            return
        
        user = user_manager.get_user(callback.from_user.id)
        
        # Получаем возможные призы из config
        from config import ROULETTE_PRIZES
        prizes = ROULETTE_PRIZES.get(ticket_id, [])
        
        # Формируем список призов
        prizes_text = "🎁 <b>Возможные призы:</b>\n"
        for prize in prizes:
            prizes_text += f"• {prize['name']}"
            if prize.get('price', 0) > 0:
                prizes_text += f" ({prize['price']}⭐)"
            prizes_text += "\n"
        
        text = f"""
🎰 {ticket['name']}

💰 <b>Цена:</b> {ticket['price']}⭐

{prizes_text}
"""
        
        await callback.message.edit_text(text, reply_markup=get_roulette_ticket_keyboard(ticket_id), parse_mode="HTML")
    except Exception as e:
        await callback.answer(f"❌ Ошибка: {str(e)}", show_alert=True)


@router.callback_query(F.data.startswith("buy_ticket_"))
async def buy_ticket(callback: CallbackQuery):
    """Купить билет - отправить счёт на оплату или дать бесплатно"""
    try:
        ticket_id = int(callback.data.split("_")[2])
        ticket = get_ticket_by_id(ticket_id)
        
        if not ticket:
            await callback.answer("❌ Билет не найден", show_alert=True)
            return
        
        # Если билет бесплатный - сразу дать его
        if ticket['price'] == 0:
            user = user_manager.get_user(callback.from_user.id)
            
            # Проверяем шанс выигрыша
            if random.randint(1, 100) <= ticket['win_chance']:
                # Пользователь выиграл! Выбираем приз по шансам
                prizes = ROULETTE_PRIZES.get(ticket_id, [])
                if prizes:
                    prize = select_prize_by_chance(prizes)
                    
                    # Сохраняем выигрыш в БД (единая функция)
                    roulette_manager.add_roulette_result(
                        telegram_id=callback.from_user.id,
                        ticket_id=ticket_id,
                        ticket_name=ticket['name'],
                        ticket_price=ticket['price'],
                        prize_name=prize['name'],
                        prize_type=prize.get('type', 'gift'),
                        prize_value=prize.get('price', 0)
                    )
                    
                    text = f"""
✅ <b>ПОЗДРАВЛЯЕМ! ВЫ ВЫИГРАЛИ!</b>

🎁 <b>Ваш приз:</b> {prize['name']}
🎰 <b>Билет:</b> {ticket['name']}

Приз скоро будет отправлен в Telegram!
"""
                else:
                    text = f"❌ Приз не найден. Обратитесь к администратору."
            else:
                # Пользователь не выиграл - сохраняем в БД
                roulette_manager.add_roulette_result(
                    telegram_id=callback.from_user.id,
                    ticket_id=ticket_id,
                    ticket_name=ticket['name'],
                    ticket_price=ticket['price'],
                    prize_name="❌ Ничего",
                    prize_type="no_prize",
                    prize_value=0
                )
                
                text = f"""
❌ <b>НЕ ПОВЕЗЛО</b>

😢 На этот раз ничего не выиграли
🎰 <b>Билет:</b> {ticket['name']}

Попробуйте ещё раз!
"""
            
            await callback.message.edit_text(text, reply_markup=get_roulette_keyboard(), parse_mode="HTML")
            return
        
        # Создать счёт для оплаты в Telegram Stars
        prices = [LabeledPrice(
            label=f"{ticket['name']} - Шанс: {ticket['win_chance']}%",
            amount=ticket['price']
        )]
        
        await callback.bot.send_invoice(
            chat_id=callback.from_user.id,
            title=f"🎰 {ticket['name']}",
            description=f"Билет рулетки. Шанс выигрыша: {ticket['win_chance']}%",
            payload=f"roulette_ticket_{ticket_id}",
            provider_token="",
            currency="XTR",
            prices=prices
        )
        
        await callback.answer("✅ Счёт отправлен!", show_alert=False)
    
    except Exception as e:
        await callback.answer(f"❌ Ошибка: {str(e)}", show_alert=True)


@router.callback_query(F.data == "roulette")
async def roulette_menu(callback: CallbackQuery):
    """Главное меню рулетки"""
    try:
        text = """
🎰 <b>РУЛЕТКА - Низкие шансы!</b>

Выбери билет на удачу:
Чем дороже - тем выше шанс!

Выигрыши - только Telegram Gifts 🎁
"""
        await callback.message.edit_text(text, reply_markup=get_roulette_keyboard(), parse_mode="HTML")
    except Exception as e:
        await callback.answer(f"❌ Ошибка: {str(e)}", show_alert=True)


@router.callback_query(F.data == "roulette_back")
async def roulette_back(callback: CallbackQuery):
    """Вернуться в главное меню"""
    try:
        user = user_manager.get_user(callback.from_user.id)
        text = f"👤 <b>Ваш профиль</b>\n\n👥 Рефералов: {user.get('total_referrals', 0)}"
        
        await callback.message.edit_text(text, reply_markup=get_main_menu_keyboard(), parse_mode="HTML")
    except Exception as e:
        await callback.answer(f"❌ Ошибка: {str(e)}", show_alert=True)
