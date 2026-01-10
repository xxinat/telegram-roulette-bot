"""
ПОЛНАЯ СТАТИСТИКА РУЛЕТКИ ПО ВСЕМ ПОЛЬЗОВАТЕЛЯМ
"""

import json
from collections import defaultdict
from datetime import datetime

# Загружаем данные
with open('bot_data/roulette_results.json', 'r', encoding='utf-8') as f:
    results = json.load(f)

with open('bot_data/users.json', 'r', encoding='utf-8') as f:
    users = json.load(f)

# Создаем словарь юзеров для быстрого поиска
users_dict = {u['id']: u for u in users}

print("=" * 100)
print("📊 ОБЩАЯ СТАТИСТИКА РУЛЕТКИ ПО ВСЕМ ПОЛЬЗОВАТЕЛЯМ")
print("=" * 100)

# Общие данные
total_spins = len(results)
total_players = len(set(r['user_id'] for r in results))

print(f"\n📈 ОБЩИЕ ПОКАЗАТЕЛИ:")
print(f"   Всего открытий: {total_spins}")
print(f"   Всего игроков: {total_players}")

if total_spins == 0:
    print("\n❌ Нет данных о рулетке")
    exit()

# Финансовая статистика
total_spent = sum(r['ticket_price'] for r in results)
total_won = sum(r.get('prize_value', 0) for r in results)
net_result = total_won - total_spent

print(f"   💰 Всего потрачено: {total_spent}")
print(f"   🎁 Всего выиграно: {total_won}")
print(f"   📊 Баланс: {'+' if net_result >= 0 else ''}{net_result}")
print(f"   📉 ROI (возврат): {(total_won / total_spent * 100):.1f}%")

# Статистика по билетам
print(f"\n🎟️ СТАТИСТИКА ПО ТИПАМ БИЛЕТОВ:")
by_ticket = defaultdict(list)
for r in results:
    by_ticket[r['ticket_name']].append(r)

ticket_stats = []
for ticket_name in sorted(by_ticket.keys()):
    ticket_results = by_ticket[ticket_name]
    ticket_price = ticket_results[0]['ticket_price']
    count = len(ticket_results)
    wins = sum(1 for r in ticket_results if r.get('prize_value', 0) > 0)
    total_value = sum(r.get('prize_value', 0) for r in ticket_results)
    win_rate = (wins / count * 100) if count > 0 else 0
    
    ticket_stats.append({
        'name': ticket_name,
        'count': count,
        'price': ticket_price,
        'wins': wins,
        'win_rate': win_rate,
        'total_value': total_value
    })

for stat in sorted(ticket_stats, key=lambda x: x['count'], reverse=True):
    print(f"\n   {stat['name']}:")
    print(f"      Открыто: {stat['count']} (цена {stat['price']} за шт)")
    print(f"      Выигрышей: {stat['wins']} ({stat['win_rate']:.1f}%)")
    print(f"      Выиграно: {stat['total_value']}")
    print(f"      Инвестировано: {stat['count'] * stat['price']}")
    print(f"      ROI: {(stat['total_value'] / (stat['count'] * stat['price']) * 100):.1f}%")

# Распределение призов
print(f"\n🎁 РАСПРЕДЕЛЕНИЕ ПРИЗОВ (ТОП 10):")
prize_distribution = defaultdict(int)
prize_value_distribution = defaultdict(int)

for result in results:
    prize_name = result['prize_name']
    prize_value = result.get('prize_value', 0)
    prize_distribution[prize_name] += 1
    prize_value_distribution[prize_name] += prize_value

prize_stats = []
for prize_name in prize_distribution.keys():
    count = prize_distribution[prize_name]
    total_value = prize_value_distribution[prize_name]
    percentage = (count / len(results) * 100) if results else 0
    avg_value = total_value / count if count > 0 else 0
    prize_stats.append({
        'name': prize_name,
        'count': count,
        'percentage': percentage,
        'total_value': total_value,
        'avg_value': avg_value
    })

for i, stat in enumerate(sorted(prize_stats, key=lambda x: x['count'], reverse=True)[:10], 1):
    print(f"\n   {i}. {stat['name']}")
    print(f"      Выпало: {stat['count']} раз ({stat['percentage']:.1f}%)")
    print(f"      Всего ед.: {stat['total_value']}")
    print(f"      Среднее: {stat['avg_value']:.1f}")

# Статистика по игрокам
print(f"\n👥 ТОП 10 ИГРОКОВ (ПО ОТКРЫТИЯМ):")
by_user = defaultdict(list)
for r in results:
    by_user[r['user_id']].append(r)

user_stats = []
for user_id, user_results in by_user.items():
    username = users_dict.get(user_id, {}).get('username', 'Unknown')
    first_name = users_dict.get(user_id, {}).get('first_name', '')
    telegram_id = users_dict.get(user_id, {}).get('telegram_id', '')
    
    count = len(user_results)
    wins = sum(1 for r in user_results if r.get('prize_value', 0) > 0)
    total_spent = sum(r['ticket_price'] for r in user_results)
    total_won = sum(r.get('prize_value', 0) for r in user_results)
    win_rate = (wins / count * 100) if count > 0 else 0
    net = total_won - total_spent
    
    user_stats.append({
        'user_id': user_id,
        'telegram_id': telegram_id,
        'username': username,
        'first_name': first_name,
        'count': count,
        'wins': wins,
        'win_rate': win_rate,
        'total_spent': total_spent,
        'total_won': total_won,
        'net': net
    })

for i, stat in enumerate(sorted(user_stats, key=lambda x: x['count'], reverse=True)[:10], 1):
    display_name = f"@{stat['username']}" if stat['username'] else stat['first_name']
    emoji = "🏆" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"  {i}."
    print(f"\n   {emoji} {display_name} (ID: {stat['telegram_id']})")
    print(f"      Открытий: {stat['count']}")
    print(f"      Выигрышей: {stat['wins']} ({stat['win_rate']:.1f}%)")
    print(f"      Потрачено: {stat['total_spent']} | Выиграно: {stat['total_won']}")
    print(f"      Баланс: {'+' if stat['net'] >= 0 else ''}{stat['net']}")

# Самые удачные игроки (по ROI)
print(f"\n💰 САМЫЕ УДАЧНЫЕ ИГРОКИ (ПО ПРИБЫЛИ):")
profitable_users = [u for u in user_stats if u['net'] > 0]
if profitable_users:
    for i, stat in enumerate(sorted(profitable_users, key=lambda x: x['net'], reverse=True)[:5], 1):
        display_name = f"@{stat['username']}" if stat['username'] else stat['first_name']
        print(f"   {i}. {display_name} (ID: {stat['telegram_id']}): +{stat['net']} ({(stat['total_won']/stat['total_spent']*100):.1f}%)")
else:
    print("   ❌ Нет игроков с прибылью")

# Статистика по типам призов
print(f"\n📦 РАЗБОР ТИПОВ ПРИЗОВ:")
prize_types = defaultdict(lambda: {'count': 0, 'total_value': 0})
for result in results:
    prize_type = result.get('prize_type', 'unknown')
    prize_value = result.get('prize_value', 0)
    prize_types[prize_type]['count'] += 1
    prize_types[prize_type]['total_value'] += prize_value

for prize_type in sorted(prize_types.keys()):
    data = prize_types[prize_type]
    percentage = (data['count'] / len(results) * 100) if results else 0
    print(f"   {prize_type.upper()}: {data['count']} ({percentage:.1f}%) = {data['total_value']} ед.")

# Сводка
print(f"\n" + "=" * 100)
print("📋 СВОДКА:")
print("=" * 100)
print(f"✅ Анализировано: {total_spins} открытий от {total_players} игроков")
if total_spins > 0:
    print(f"📊 Среднее открытий на игрока: {(total_spins / total_players):.1f}")
    print(f"💹 Средний выигрыш на попытку: {(total_won / total_spins):.1f}")
    print(f"💰 Средние затраты на попытку: {(total_spent / total_spins):.1f}")

print("=" * 100)
