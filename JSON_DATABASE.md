# 📊 JSON База данных - Инструкция

## Что изменилось?

Вместо SQLite с SQLAlchemy теперь используется **JSON-based хранилище данных**.

### Преимущества JSON:
✅ Не требует установки БД  
✅ Легче развёртывать  
✅ Файлы можно редактировать вручную  
✅ Не нужен SQLAlchemy  
✅ Проще для небольших проектов  

---

## 📁 Структура данных

После первого запуска бота создастся папка `bot_data/` со следующими файлами:

```
bot_data/
├── users.json              # Информация о пользователях
├── purchases.json          # История покупок
├── transactions.json       # Все финансовые операции
├── referrals.json          # Данные рефералов
└── roulette_results.json   # Результаты рулетки
```

---

## 📋 Формат данных

### users.json
```json
[
  {
    "id": 1,
    "telegram_id": 123456789,
    "username": "john_doe",
    "first_name": "John",
    "last_name": "Doe",
    "stars": 100,
    "bears": 0,
    "referral_code": "ABC12345",
    "referred_by": null,
    "subscription_verified": false,
    "created_at": "2026-01-09T12:00:00.000000",
    "updated_at": "2026-01-09T12:00:00.000000"
  }
]
```

### purchases.json
```json
[
  {
    "id": 1,
    "user_id": 1,
    "item_id": 1,
    "item_name": "Шоколад 🍫",
    "item_price": 10,
    "purchase_type": "shop",
    "created_at": "2026-01-09T12:05:00.000000"
  }
]
```

### transactions.json
```json
[
  {
    "id": 1,
    "user_id": 1,
    "transaction_type": "stars_earned",
    "amount": 100,
    "description": "Регистрация",
    "created_at": "2026-01-09T12:00:00.000000"
  }
]
```

### referrals.json
```json
[
  {
    "id": 1,
    "referrer_id": 1,
    "referred_user_id": 2,
    "referred_username": "jane_doe",
    "bonus_paid": false,
    "created_at": "2026-01-09T12:10:00.000000"
  }
]
```

### roulette_results.json
```json
[
  {
    "id": 1,
    "user_id": 1,
    "ticket_id": 1,
    "ticket_name": "Обычный билет",
    "ticket_price": 10,
    "prize_name": "5 звёзд ⭐",
    "prize_type": "stars",
    "prize_value": 5,
    "created_at": "2026-01-09T12:15:00.000000"
  }
]
```

---

## 🔧 Как использовать

### Импорт менеджеров в обработчиках:

```python
from database.db_json import user_manager, purchase_manager, referral_manager, roulette_manager

# Получить или создать пользователя
user = user_manager.get_or_create_user(
    telegram_id=123456789,
    username="john_doe",
    first_name="John",
    last_name="Doe"
)

# Получить пользователя
user = user_manager.get_user(123456789)

# Добавить звёзды
user_manager.add_stars(123456789, amount=10, description="Приз")

# Вычесть звёзды
success = user_manager.subtract_stars(123456789, amount=5)

# Добавить медведей
user_manager.add_bears(123456789, amount=1)

# Получить баланс
stars, bears = user_manager.get_user_balance(123456789)

# Проверить подписку
user_manager.verify_subscription(123456789)

# Добавить покупку
purchase_manager.add_purchase(
    telegram_id=123456789,
    item_id=1,
    item_name="Шоколад 🍫",
    item_price=10,
    purchase_type="shop"
)

# Добавить реферала
referral_manager.add_referral(
    referrer_id=1,
    referred_user_id=2,
    referred_username="jane_doe"
)

# Добавить результат рулетки
roulette_manager.add_roulette_result(
    telegram_id=123456789,
    ticket_id=1,
    ticket_name="Обычный билет",
    ticket_price=10,
    prize_name="5 звёзд ⭐",
    prize_type="stars",
    prize_value=5
)
```

---

## 🔄 Миграция с SQLite

Если у вас уже была база данных SQLite, можно создать скрипт миграции:

```python
# migrate_to_json.py
import sqlite3
import json
from pathlib import Path
from database.db_json import db

# Экспортировать из SQLite
conn = sqlite3.connect('bot_data.db')
cursor = conn.cursor()

# Пример для таблицы users
cursor.execute('SELECT * FROM users')
columns = [description[0] for description in cursor.description]
users = []
for row in cursor.fetchall():
    user_dict = dict(zip(columns, row))
    users.append(user_dict)

# Сохранить в JSON
with open('bot_data/users.json', 'w') as f:
    json.dump(users, f, indent=2, default=str)

conn.close()
```

---

## 📊 Просмотр данных

### Просмотр всех пользователей:
```bash
cat bot_data/users.json
```

### Просмотр всех покупок:
```bash
cat bot_data/purchases.json
```

### Поиск пользователя:
```bash
grep -i "username" bot_data/users.json
```

---

## 🛡️ Безопасность и резервные копии

### Создать резервную копию:
```bash
# Linux/Mac
cp -r bot_data bot_data_backup_$(date +%Y%m%d)

# Windows PowerShell
Copy-Item -Path "bot_data" -Destination "bot_data_backup_$(Get-Date -Format yyyyMMdd)" -Recurse
```

### Восстановить из резервной копии:
```bash
# Linux/Mac
rm -rf bot_data
cp -r bot_data_backup_20260109 bot_data

# Windows PowerShell
Remove-Item -Path "bot_data" -Recurse -Force
Copy-Item -Path "bot_data_backup_20260109" -Destination "bot_data" -Recurse
```

### Расписание автоматических резервных копий:

**Linux (crontab):**
```bash
# Каждый день в 3:00 ночи
0 3 * * * cp -r /path/to/bot_data /path/to/backups/bot_data_$(date +\%Y\%m\%d)
```

**Windows (Task Scheduler):**
```powershell
# Создать задачу
$trigger = New-ScheduledTaskTrigger -Daily -At 3am
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "Copy-Item -Path 'D:\wwstrela\bot_data' -Destination 'D:\backups\bot_data_$(Get-Date -Format yyyyMMdd)' -Recurse"
Register-ScheduledTask -TaskName "BackupBotData" -Trigger $trigger -Action $action
```

---

## 🔍 Отладка и мониторинг

### Просмотр последних операций:
```python
import json

with open('bot_data/transactions.json', 'r') as f:
    transactions = json.load(f)
    for trans in transactions[-10:]:  # Последние 10
        print(f"{trans['created_at']}: {trans['description']}")
```

### Проверить целостность данных:
```python
import json
from pathlib import Path

for file in Path('bot_data').glob('*.json'):
    try:
        with open(file, 'r') as f:
            json.load(f)
        print(f"✅ {file.name} - OK")
    except json.JSONDecodeError:
        print(f"❌ {file.name} - ОШИБКА!")
```

---

## 💡 Советы и трюки

### Экспортировать данные в CSV:
```python
import json
import csv

with open('bot_data/users.json', 'r') as f:
    users = json.load(f)

with open('users_export.csv', 'w', newline='', encoding='utf-8') as f:
    if users:
        writer = csv.DictWriter(f, fieldnames=users[0].keys())
        writer.writeheader()
        writer.writerows(users)
```

### Получить статистику:
```python
import json
from collections import Counter

with open('bot_data/transactions.json', 'r') as f:
    transactions = json.load(f)

# Подсчитать типы транзакций
types = Counter(t['transaction_type'] for t in transactions)
print(types)

# Сумма заработанных звёзд
earned_stars = sum(t['amount'] for t in transactions if t['transaction_type'] == 'stars_earned')
print(f"Всего заработано: {earned_stars}⭐")
```

---

## ⚠️ Ограничения JSON

- ❌ Не оптимизирована для больших объёмов данных (10000+ записей)
- ❌ Нет встроенной защиты от одновременного доступа
- ❌ Медленнее чем SQL БД для сложных запросов

**Решение:** Если проект растёт, перейдите на PostgreSQL или MySQL!

---

## 🔄 Переход на SQL БД

Если нужно перейти с JSON на SQL:

```python
# Обновить импорт в main.py
from database.db_manager import init_db, UserManager, ...  # вместо db_json

# Обновить импорты в обработчиках
from database.db_manager import UserManager  # вместо db_json
```

Остальной код остаётся без изменений благодаря одинаковому API!

---

## 📞 Поддержка

Если у вас есть проблемы:
1. Проверьте формат JSON (используйте `python -m json.tool bot_data/users.json`)
2. Проверьте права доступа на файлы
3. Создайте резервную копию перед тем как редактировать вручную

---

**Статус:** ✅ JSON БД полностью интегрирована и готова к использованию!
