"""
СПИСОК ВСЕХ ВЫИГРЫШЕЙ ДЛЯ ОТПРАВКИ ПРИЗОВ
(Только выигрыши из отдельного файла roulette_wins.json)
"""

import json
from collections import defaultdict
from datetime import datetime

# Загружаем данные
with open('bot_data/roulette_wins.json', 'r', encoding='utf-8') as f:
    wins = json.load(f)

print("=" * 110)
print("🎁 ВЫИГРЫШИ ДЛЯ ОТПРАВКИ ПРИЗОВ")
print("=" * 110)

if not wins:
    print("\n❌ Выигрышей не найдено")
    exit()

print(f"\n📊 Всего выигрышей: {len(wins)}")

# Фильтруем по статусу
pending = [w for w in wins if w.get('status') == 'pending']
sent = [w for w in wins if w.get('status') == 'sent']
rejected = [w for w in wins if w.get('status') == 'rejected']

print(f"⏳ Ожидают отправки: {len(pending)}")
print(f"✅ Отправлены: {len(sent)}")
print(f"❌ Отклонены: {len(rejected)}")

# Группируем по статусу
print(f"\n{'=' * 110}")
print("📋 ОЖИДАЮЩИЕ ОТПРАВКИ (⏳ PENDING):")
print("=" * 110)

if pending:
    for i, win in enumerate(pending, 1):
        timestamp = win['created_at'].split('T')[1][:8]
        display_name = f"@{win['username']}" if win['username'] else win['first_name']
        
        print(f"\n   {i}. 🎁 {win['prize_name']}")
        print(f"      👤 Пользователь: {display_name}")
        print(f"      🆔 Telegram ID: {win['telegram_id']}")
        print(f"      📱 Имя: {win['first_name']}")
        print(f"      🎟️ Билет: {win['ticket_name']}")
        print(f"      ⭐ Стоимость приза: {win['prize_value']}")
        print(f"      🕐 Время выигрыша: {timestamp}")
        print(f"      📌 ID выигрыша: {win['id']}")
else:
    print("\n✅ Все выигрыши отправлены!")

# Отправленные
if sent:
    print(f"\n{'=' * 110}")
    print(f"✅ ОТПРАВЛЕННЫЕ ПРИЗЫ:")
    print("=" * 110)
    
    for i, win in enumerate(sent, 1):
        timestamp = win['created_at'].split('T')[1][:8]
        display_name = f"@{win['username']}" if win['username'] else win['first_name']
        
        print(f"\n   {i}. ✅ {win['prize_name']}")
        print(f"      👤 {display_name} (ID: {win['telegram_id']})")

# Отклоненные
if rejected:
    print(f"\n{'=' * 110}")
    print(f"❌ ОТКЛОНЕННЫЕ ПРИЗЫ:")
    print("=" * 110)
    
    for i, win in enumerate(rejected, 1):
        timestamp = win['created_at'].split('T')[1][:8]
        display_name = f"@{win['username']}" if win['username'] else win['first_name']
        
        print(f"\n   {i}. ❌ {win['prize_name']}")
        print(f"      👤 {display_name} (ID: {win['telegram_id']})")

# Статистика по призам
print(f"\n{'=' * 110}")
print("📊 СТАТИСТИКА ПО ПРИЗАМ:")
print("=" * 110)

prize_stats = defaultdict(lambda: {'count': 0, 'value': 0, 'pending': 0, 'sent': 0})
for win in wins:
    prize_name = win['prize_name']
    prize_stats[prize_name]['count'] += 1
    prize_stats[prize_name]['value'] += win['prize_value']
    if win['status'] == 'pending':
        prize_stats[prize_name]['pending'] += 1
    elif win['status'] == 'sent':
        prize_stats[prize_name]['sent'] += 1

print()
for prize, stats in sorted(prize_stats.items(), key=lambda x: x[1]['count'], reverse=True):
    status_icon = "⏳" if stats['pending'] > 0 else "✅"
    print(f"   {status_icon} {prize}: {stats['count']} шт (⏳ {stats['pending']}, ✅ {stats['sent']})")

print(f"\n{'=' * 110}")
