"""
ТЕСТ СИМУЛЯЦИИ ПРЯМО НА ТЕКУЩЕМ КОДЕ
"""

import random
from bot.config import ROULETTE_TICKETS, ROULETTE_PRIZES

def select_prize_by_chance(prizes: list):
    """Копия функции из обработчика"""
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
    
    return prizes[-1]

def test_roulette(ticket_id, spins=1000):
    """Симулировать открытие рулетки"""
    ticket = next((t for t in ROULETTE_TICKETS if t['id'] == ticket_id), None)
    if not ticket:
        return None
    
    wins = 0
    for _ in range(spins):
        # Первый уровень: шанс выигрыша билета
        if random.randint(1, 100) <= ticket['win_chance']:
            # Второй уровень: выбираем приз
            prizes = ROULETTE_PRIZES.get(ticket_id, [])
            if prizes:
                prize = select_prize_by_chance(prizes)
                if prize:
                    wins += 1
    
    return wins, spins

print("=" * 80)
print("🧪 ТЕСТ СИМУЛЯЦИИ РУЛЕТКИ")
print("=" * 80)

# Тест билета ID 1 (Обычный, 30% шанс)
print("\n🎟️ Тест ОБЫЧНОГО БИЛЕТА (30% ожидается):")
for test_num in range(3):
    wins, total = test_roulette(1, 1000)
    win_rate = (wins / total * 100)
    print(f"   Тест {test_num+1}: {wins}/{total} = {win_rate:.1f}%")

# Проверяем: может быть проблема что система ВСЕГДА возвращает None?
print("\n🔍 ПРОВЕРКА: может ли система вернуть None?")
prizes = ROULETTE_PRIZES.get(1, [])
print(f"   Призы для билета 1: {len(prizes)} шт")
for i in range(5):
    prize = select_prize_by_chance(prizes)
    if prize:
        print(f"   {i+1}. ✅ {prize['name']}")
    else:
        print(f"   {i+1}. ❌ ОШИБКА: prize is None!")

print("\n" + "=" * 80)
