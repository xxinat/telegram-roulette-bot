"""
Отметить выигрыш как отправленный
Использование: python mark_win_sent.py <win_id> [sent|rejected]
Например: python mark_win_sent.py 1 sent
         python mark_win_sent.py 2 rejected
"""

import json
import sys
from datetime import datetime

if len(sys.argv) < 2:
    print("❌ Использование: python mark_win_sent.py <win_id> [sent|rejected]")
    print("   Пример: python mark_win_sent.py 1 sent")
    sys.exit(1)

try:
    win_id = int(sys.argv[1])
    status = sys.argv[2].lower() if len(sys.argv) > 2 else 'sent'
    
    if status not in ['sent', 'rejected']:
        print(f"❌ Неверный статус: {status}. Используйте 'sent' или 'rejected'")
        sys.exit(1)
        
except ValueError:
    print(f"❌ Неверный ID: {sys.argv[1]}")
    sys.exit(1)

# Загружаем выигрыши
with open('bot_data/roulette_wins.json', 'r', encoding='utf-8') as f:
    wins = json.load(f)

# Ищем выигрыш
found = False
for win in wins:
    if win.get('id') == win_id:
        old_status = win.get('status')
        win['status'] = status
        win['updated_at'] = datetime.now().isoformat()
        found = True
        
        # Сохраняем
        with open('bot_data/roulette_wins.json', 'w', encoding='utf-8') as f:
            json.dump(wins, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Выигрыш #{win_id} обновлен: {old_status} → {status}")
        print(f"   🎁 Приз: {win['prize_name']}")
        print(f"   👤 Пользователь: @{win['username']} (ID: {win['telegram_id']})")
        print(f"   ⭐ Стоимость: {win['prize_value']}")
        break

if not found:
    print(f"❌ Выигрыш #{win_id} не найден")
    print("\nДоступные выигрыши:")
    
    # Показываем все выигрыши
    for win in wins:
        status_emoji = '⏳' if win.get('status') == 'pending' else '✅' if win.get('status') == 'sent' else '❌'
        print(f"   {status_emoji} #{win['id']}: {win['prize_name']} для @{win['username']}")
