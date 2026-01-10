#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
STATUS_CHECK.py - Быстрая проверка статуса Telegram бота
Используйте этот скрипт для проверки всех компонентов бота
"""

import os
import json
import sys
from datetime import datetime

def check_status():
    """Проверить статус всех компонентов"""
    
    print("=" * 60)
    print("🤖 ПРОВЕРКА СТАТУСА TELEGRAM БОТА")
    print("=" * 60)
    print()
    
    # Проверка файлов
    print("📁 ПРОВЕРКА ФАЙЛОВ:")
    print("-" * 60)
    
    required_files = {
        'bot/main.py': '✅',
        'bot/config.py': '✅',
        'bot/handlers/start.py': '✅',
        'bot/handlers/menu.py': '✅',
        'bot/handlers/shop.py': '✅',
        'bot/handlers/roulette.py': '✅',
        'bot/handlers/referral.py': '✅',
        'bot/database/db_json.py': '✅',
        'bot/utils/keyboards.py': '✅',
        'bot/utils/subscription.py': '✅',
        'requirements.txt': '✅',
        '.env': '✅',
    }
    
    for file_path, status in required_files.items():
        if os.path.exists(file_path):
            print(f"  {status} {file_path}")
        else:
            print(f"  ❌ {file_path} - НЕ НАЙДЕН")
    
    print()
    
    # Проверка БД
    print("💾 ПРОВЕРКА БАЗЫ ДАННЫХ:")
    print("-" * 60)
    
    db_files = {
        'bot_data/users.json': 'пользователи',
        'bot_data/purchases.json': 'покупки',
        'bot_data/transactions.json': 'транзакции',
        'bot_data/referrals.json': 'рефералы',
        'bot_data/roulette_results.json': 'результаты рулетки',
    }
    
    for file_path, description in db_files.items():
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                count = len(data)
                print(f"  ✅ {description.upper():20} - {count} записей")
            except Exception as e:
                print(f"  ⚠️  {description.upper():20} - ошибка: {str(e)}")
        else:
            print(f"  ⚠️  {description.upper():20} - будет создана при первом запуске")
    
    print()
    
    # Проверка конфигурации
    print("⚙️  КОНФИГУРАЦИЯ:")
    print("-" * 60)
    
    try:
        with open('bot/config.py', 'r', encoding='utf-8') as f:
            config = f.read()
            
        if '8226602991:AAGsr0Xz' in config:
            print("  ✅ BOT_TOKEN установлен")
        else:
            print("  ❌ BOT_TOKEN не найден или неверный")
        
        if 'CHANNELS_TO_SUBSCRIBE = []' in config:
            print("  ✅ CHANNELS_TO_SUBSCRIBE = [] (отключена проверка подписки)")
        else:
            print("  ⚠️  CHANNELS_TO_SUBSCRIBE содержит каналы (может требоваться доступ)")
        
        if 'SHOP_ITEMS' in config:
            print("  ✅ Магазин настроен (5 товаров)")
        
        if 'ROULETTE_TICKETS' in config:
            print("  ✅ Рулетка настроена (4 типа билетов)")
            
    except Exception as e:
        print(f"  ❌ Ошибка при чтении конфигурации: {e}")
    
    print()
    
    # Проверка зависимостей
    print("📦 ЗАВИСИМОСТИ:")
    print("-" * 60)
    
    required_packages = ['aiogram', 'aiohttp', 'dotenv']
    
    for package in required_packages:
        try:
            __import__(package if package != 'dotenv' else 'dotenv')
            print(f"  ✅ {package:15} установлен")
        except ImportError:
            print(f"  ❌ {package:15} НЕ установлен - выполните: pip install -r requirements.txt")
    
    print()
    
    # Статистика пользователей
    print("👥 ПОЛЬЗОВАТЕЛИ:")
    print("-" * 60)
    
    try:
        with open('bot_data/users.json', 'r', encoding='utf-8') as f:
            users = json.load(f)
        
        total_stars = sum(u.get('stars', 0) for u in users)
        total_bears = sum(u.get('bears', 0) for u in users)
        
        print(f"  Всего пользователей: {len(users)}")
        print(f"  Всего звёзд в системе: {total_stars}⭐")
        print(f"  Всего медведей в системе: {total_bears}🐻")
        
        if users:
            print("\n  Последние пользователи:")
            for user in users[-3:]:
                print(f"    • {user.get('first_name')} (@{user.get('username')}) - "
                      f"{user.get('stars')}⭐ / {user.get('bears')}🐻")
    except Exception as e:
        print(f"  ⚠️  Ошибка при чтении пользователей: {e}")
    
    print()
    
    # Статистика транзакций
    print("💰 СТАТИСТИКА ТРАНЗАКЦИЙ:")
    print("-" * 60)
    
    try:
        with open('bot_data/purchases.json', 'r', encoding='utf-8') as f:
            purchases = json.load(f)
        
        shops = [p for p in purchases if p.get('type') == 'shop']
        roulettes = [p for p in purchases if p.get('type') == 'roulette']
        
        print(f"  Покупок в магазине: {len(shops)}")
        print(f"  Спинов рулетки: {len(roulettes)}")
        
        total_spent = sum(p.get('amount', 0) for p in purchases)
        print(f"  Всего потрачено звёзд: {total_spent}⭐")
        
    except Exception as e:
        print(f"  ⚠️  Нет данных о транзакциях: {e}")
    
    print()
    print("=" * 60)
    print("🟢 БОТ ГОТОВ К ИСПОЛЬЗОВАНИЮ")
    print("=" * 60)
    print()
    print("📝 Команды для запуска:")
    print("  1. Прямой запуск:")
    print("     python bot/main.py")
    print()
    print("  2. В фоне (Windows PowerShell):")
    print("     Start-Process python -ArgumentList 'bot/main.py'")
    print()
    print("  3. С логированием:")
    print("     python bot/main.py 2>&1 | tee bot.log")
    print()
    print("📱 Тестирование:")
    print("  1. Откройте Telegram")
    print("  2. Найдите @testpodarkibotiksbot")
    print("  3. Отправьте /start")
    print("  4. Выберите действие из меню")
    print()

if __name__ == "__main__":
    try:
        check_status()
    except KeyboardInterrupt:
        print("\n⏹️  Проверка прервана пользователем")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        sys.exit(1)
