"""
СПИСОК ВСЕХ ВЫИГРЫШЕЙ (ДЛЯ ОТПРАВКИ ПРИЗОВ)
"""

import json
from collections import defaultdict

# Загружаем данные
with open('bot_data/roulette_results.json', 'r', encoding='utf-8') as f:
    results = json.load(f)

print("=" * 100)
print("🎁 СПИСОК ВСЕХ ВЫИГРЫШЕЙ (ДЛЯ ОТПРАВКИ ПРИЗОВ)")
print("=" * 100)

# Фильтруем только выигрыши
wins = [r for r in results if r.get('prize_type') != 'no_prize']

print(f"\n📊 Всего выигрышей: {len(wins)}")
print(f"Всего рулеток открыто: {len(results)}")
print(f"Процент выигрышей: {(len(wins)/len(results)*100):.1f}%")

if not wins:
    print("\n❌ Выигрышей не найдено")
    exit()

# Группируем по пользователям
by_user = defaultdict(list)
for win in wins:
    key = (win.get('telegram_id'), win.get('username', 'unknown'), win.get('first_name', ''))
    by_user[key].append(win)

print(f"\n👥 ВЫИГРЫШИ ПО ПОЛЬЗОВАТЕЛЯМ:\n")

for (telegram_id, username, first_name), user_wins in sorted(by_user.items(), key=lambda x: len(x[1]), reverse=True):
    display_name = f"@{username}" if username else first_name
    print(f"{'=' * 100}")
    print(f"📱 Пользователь: {display_name}")
    print(f"🆔 Telegram ID: {telegram_id}")
    print(f"📝 Имя: {first_name}")
    print(f"📊 Всего выигрышей: {len(user_wins)}")
    print(f"{'─' * 100}")
    
    # Выигрыши по датам
    for i, win in enumerate(sorted(user_wins, key=lambda x: x['created_at']), 1):
        timestamp = win['created_at'].split('T')[1][:8]
        print(f"\n   {i}. 🎁 {win['prize_name']}")
        print(f"      🎟️ Билет: {win['ticket_name']} ({win['ticket_price']})")
        print(f"      ⭐ Стоимость приза: {win['prize_value']}")
        print(f"      🕐 Время: {timestamp}")

print(f"\n{'=' * 100}")
print("📋 СВОДКА:")
print("=" * 100)

# Суммируем по типам призов
prize_summary = defaultdict(int)
for win in wins:
    prize_summary[win['prize_name']] += 1

print("\n🎁 ТОП ВЫИГРЫШЕЙ:")
for prize, count in sorted(prize_summary.items(), key=lambda x: x[1], reverse=True):
    print(f"   {prize}: {count} раз")

print("\n" + "=" * 100)
