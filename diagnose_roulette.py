"""
ДИАГНОСТИКА СИСТЕМЫ ВЕРОЯТНОСТИ
"""

import json
from bot.config import ROULETTE_TICKETS, ROULETTE_PRIZES

print("=" * 80)
print("🔍 ДИАГНОСТИКА КОНФИГУРАЦИИ")
print("=" * 80)

# Проверяем билеты
print("\n🎟️ КОНФИГУРАЦИЯ БИЛЕТОВ:")
for ticket in ROULETTE_TICKETS:
    print(f"\n   ID {ticket['id']}: {ticket['name']}")
    print(f"      Цена: {ticket['price']}")
    print(f"      Шанс выигрыша: {ticket['win_chance']}%")
    
    # Проверяем наличие призов
    prizes = ROULETTE_PRIZES.get(ticket['id'])
    if prizes:
        print(f"      ✅ Призы найдены ({len(prizes)} шт):")
        total_drop_chance = sum(p.get('drop_chance', 0) for p in prizes)
        print(f"         Всего шансов на выигрыш: {total_drop_chance}%")
        for p in prizes:
            print(f"         - {p['name']}: {p.get('drop_chance', '?')}%")
    else:
        print(f"      ❌ ОШИБКА: Нет призов!")

print("\n" + "=" * 80)
print("📊 СТАТИСТИКА НОВЫХ ОТКРЫТИЙ")
print("=" * 80)

# Загружаем реальные данные
with open('bot_data/roulette_results.json', 'r', encoding='utf-8') as f:
    results = json.load(f)

# Берем новые результаты (с новой датой)
new_results = [r for r in results if r['created_at'] >= '2026-01-10T18:']

print(f"\nВсего новых открытий: {len(new_results)}")
print(f"Выигрышей: {len([r for r in new_results if r['prize_type'] != 'no_prize'])}")
print(f"Проигрышей: {len([r for r in new_results if r['prize_type'] == 'no_prize'])}")

# Анализируем
print(f"\nРаспределение:")
for r in new_results:
    timestamp = r['created_at'].split('T')[1]
    status = "✅" if r['prize_type'] != 'no_prize' else "❌"
    print(f"   {timestamp}: {status} {r['prize_name']}")

print("\n" + "=" * 80)
print("⚠️  АНАЛИЗ:")
print("=" * 80)

if len(new_results) > 0:
    win_rate = (len([r for r in new_results if r['prize_type'] != 'no_prize']) / len(new_results)) * 100
    print(f"Текущий процент выигрышей: {win_rate:.1f}%")
    print(f"Ожидается ~30% при 100+ открытиях")
    
    if win_rate < 5:
        print("\n🔴 ВНИМАНИЕ: Выигрышей слишком мало!")
        print("Возможные причины:")
        print("1. Случайная неудача (вероятность ~2.8% при 10 открытиях)")
        print("2. Ошибка в логике системы вероятности")
        print("3. Проблема с импортом конфигурации")
