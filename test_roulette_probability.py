"""
Тестирование системы вероятности рулетки
"""

import random

# Конфиг билетов
ROULETTE_TICKETS = [
    {"id": 1, "name": "🎟️ Обычный билет", "price": 0, "win_chance": 30},
    {"id": 2, "name": "🎫 Серебряный билет", "price": 49, "win_chance": 40},
    {"id": 3, "name": "🏆 Золотой билет", "price": 99, "win_chance": 50},
    {"id": 4, "name": "👑 Платиновый билет", "price": 149, "win_chance": 60},
]

ROULETTE_PRIZES = {
    1: [
        {"name": "🧸 Мишка", "drop_chance": 50},
        {"name": "🌹 Роза", "drop_chance": 30},
        {"name": "🍾 Шампанское", "drop_chance": 15},
        {"name": "💎 Алмаз", "drop_chance": 5},
    ],
}


def select_prize_by_chance(prizes):
    """Выбрать приз по шансам"""
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


def simulate_roulette(ticket_id, spins=1000):
    """Симулировать N спинов рулетки"""
    ticket = next((t for t in ROULETTE_TICKETS if t['id'] == ticket_id), None)
    if not ticket:
        return None
    
    wins = 0
    prize_counts = {}
    
    for _ in range(spins):
        # Первый уровень: шанс выигрыша
        if random.randint(1, 100) <= ticket['win_chance']:
            wins += 1
            # Второй уровень: выбор приза
            prizes = ROULETTE_PRIZES.get(ticket_id, [])
            if prizes:
                prize = select_prize_by_chance(prizes)
                prize_name = prize['name']
                prize_counts[prize_name] = prize_counts.get(prize_name, 0) + 1
    
    return {
        'ticket': ticket['name'],
        'total_spins': spins,
        'wins': wins,
        'win_rate': f"{(wins / spins * 100):.1f}%",
        'prizes': prize_counts
    }


if __name__ == "__main__":
    print("=" * 70)
    print("ТЕСТИРОВАНИЕ СИСТЕМЫ ВЕРОЯТНОСТИ РУЛЕТКИ")
    print("=" * 70)
    
    # Тестируем обычный билет с 1000 спинов
    result = simulate_roulette(ticket_id=1, spins=1000)
    
    print(f"\n🎰 {result['ticket']}")
    print(f"📊 Всего спинов: {result['total_spins']}")
    print(f"🎯 Выигрышей: {result['wins']} (ожидаемо ~{int(300)}, получено {result['win_rate']})")
    print(f"\n💎 Распределение призов из {result['wins']} выигрышей:")
    
    for prize_name, count in sorted(result['prizes'].items(), key=lambda x: x[1], reverse=True):
        pct = (count / result['wins'] * 100) if result['wins'] > 0 else 0
        print(f"   {prize_name}: {count} раз ({pct:.1f}%)")
    
    print("\n" + "=" * 70)
    print("ВЫВОД:")
    print("=" * 70)
    print("✅ Если у вас 20-30 спинов - это НОРМАЛЬНО не выиграть ничего!")
    print("📈 При 1000 спинов - видна реальная вероятность")
    print("=" * 70)
