"""
Анализ статистики открытий рулетки
"""

import json
from collections import defaultdict
from datetime import datetime

# Загружаем данные
with open('bot_data/roulette_results.json', 'r', encoding='utf-8') as f:
    results = json.load(f)

with open('bot_data/users.json', 'r', encoding='utf-8') as f:
    users = json.load(f)

# Находим вашего пользователя (ID 1 или стormblazzko)
your_user_id = 1
user = next((u for u in users if u['id'] == your_user_id), None)

if not user:
    print("❌ Пользователь не найден")
    exit()

print("=" * 80)
print(f"📊 СТАТИСТИКА РУЛЕТКИ")
print(f"Пользователь: @{user['username']} ({user['first_name']})")
print("=" * 80)

# Фильтруем результаты вашего пользователя
your_results = [r for r in results if r['user_id'] == your_user_id]

print(f"\n📈 ОБЩИЕ ДАННЫЕ:")
print(f"   Всего открытий: {len(your_results)}")

if not your_results:
    print("\n❌ У вас нет результатов рулетки в базе")
    print("Это может быть потому что:")
    print("• Данные еще не синхронизировались")
    print("• Используется новая система с Telegram Stars")
    print("• Нужно перезапустить бота и открыть кейсы снова")
    exit()

# Подсчитываем затраты и выигрыши
total_spent = sum(r['ticket_price'] for r in your_results)
total_won = sum(r.get('prize_value', 0) for r in your_results)
net_profit = total_won - total_spent

# Анализируем призы
prize_distribution = defaultdict(int)
prize_value_distribution = defaultdict(int)

for result in your_results:
    prize_name = result['prize_name']
    prize_value = result.get('prize_value', 0)
    prize_distribution[prize_name] += 1
    prize_value_distribution[prize_name] += prize_value

print(f"   💰 Потрачено: {total_spent} звёзд/медведей")
print(f"   🎁 Выигрышей: {total_won} звёзд/медведей")
print(f"   📊 Баланс: {'+' if net_profit >= 0 else ''}{net_profit}")

# Процент выигрыша по типам билетов
print(f"\n🎟️ РЕЗУЛЬТАТЫ ПО ТИПАМ БИЛЕТОВ:")
by_ticket = defaultdict(list)
for r in your_results:
    by_ticket[r['ticket_name']].append(r)

for ticket_name in sorted(by_ticket.keys()):
    ticket_results = by_ticket[ticket_name]
    ticket_price = ticket_results[0]['ticket_price']
    count = len(ticket_results)
    total_value = sum(r.get('prize_value', 0) for r in ticket_results)
    
    print(f"\n   {ticket_name} ({ticket_price} за шт):")
    print(f"      Всего открыто: {count}")
    print(f"      Всего выиграно: {total_value}")
    print(f"      Средний выигрыш: {total_value / count:.1f}")

# Распределение призов
print(f"\n🎁 РАСПРЕДЕЛЕНИЕ ПРИЗОВ:")
for prize_name in sorted(prize_distribution.keys(), key=lambda x: prize_distribution[x], reverse=True):
    count = prize_distribution[prize_name]
    total_value = prize_value_distribution[prize_name]
    percentage = (count / len(your_results) * 100) if your_results else 0
    
    print(f"   {prize_name}: {count} раз ({percentage:.1f}%) = {total_value} ед.")

# Временная статистика
if your_results:
    first_date = datetime.fromisoformat(your_results[0]['created_at'])
    last_date = datetime.fromisoformat(your_results[-1]['created_at'])
    
    print(f"\n📅 ВРЕМЕННАЯ ИНФОРМАЦИЯ:")
    print(f"   Первое открытие: {first_date.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   Последнее открытие: {last_date.strftime('%Y-%m-%d %H:%M:%S')}")

print("\n" + "=" * 80)
print("⚠️  ВАЖНО:")
print("=" * 80)
print("Эта статистика основана на СТАРЫХ данных (до обновления системы)")
print("Новые открытия с Telegram Stars еще не отображаются в этом отчете")
print("Для актуальной информации проверьте боте_data/purchases.json")
print("=" * 80)
