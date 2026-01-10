"""
JSON-based система хранения данных для бота
Альтернатива SQLAlchemy + SQLite
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from uuid import uuid4
from pathlib import Path


class JSONDatabase:
    """Менеджер JSON базы данных"""
    
    def __init__(self, data_dir: str = "bot_data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # Пути к JSON файлам
        self.users_file = self.data_dir / "users.json"
        self.purchases_file = self.data_dir / "purchases.json"
        self.transactions_file = self.data_dir / "transactions.json"
        self.referrals_file = self.data_dir / "referrals.json"
        self.roulette_file = self.data_dir / "roulette_results.json"
        self.roulette_wins_file = self.data_dir / "roulette_wins.json"  # Только выигрыши
        
        # Инициализировать файлы
        self._init_files()
    
    def _init_files(self):
        """Создать JSON файлы если их нет"""
        files = [
            self.users_file,
            self.purchases_file,
            self.transactions_file,
            self.referrals_file,
            self.roulette_file,
            self.roulette_wins_file
        ]
        
        for file in files:
            if not file.exists():
                with open(file, 'w', encoding='utf-8') as f:
                    json.dump([], f, ensure_ascii=False, indent=2)
    
    def _read_json(self, file_path: Path) -> List:
        """Прочитать JSON файл"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def _write_json(self, file_path: Path, data: List):
        """Записать JSON файл"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def generate_referral_code(self) -> str:
        """Генерировать уникальный реф. код"""
        return str(uuid4())[:8].upper()


class UserManager(JSONDatabase):
    """Менеджер пользователей"""
    
    def get_or_create_user(self, telegram_id: int, username: str = None, 
                          first_name: str = None, last_name: str = None) -> Dict:
        """Получить или создать пользователя"""
        from config import STARTING_STARS, STARTING_BEARS
        
        users = self._read_json(self.users_file)
        
        # Поиск существующего пользователя
        user = next((u for u in users if u['telegram_id'] == telegram_id), None)
        
        if user:
            # Обновить информацию
            if username:
                user['username'] = username
            if first_name:
                user['first_name'] = first_name
            if last_name:
                user['last_name'] = last_name
            user['updated_at'] = datetime.utcnow().isoformat()
            self._write_json(self.users_file, users)
            return user
        
        # Создать нового пользователя с нулевым балансом
        new_user = {
            'id': len(users) + 1,
            'telegram_id': telegram_id,
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'stars': STARTING_STARS,  # 0 - чистый аккаунт
            'bears': STARTING_BEARS,  # 0 - без подарков
            'referral_code': self.generate_referral_code(),
            'referred_by': None,
            'subscription_verified': False,
            'total_referrals': 0,  # Всего пригласил людей
            'active_referrals': 0,  # Активных рефералов
            'gifts_earned': 0,  # Подарков получено за рефералы
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        }
        
        users.append(new_user)
        self._write_json(self.users_file, users)
        return new_user
    
    def get_user(self, telegram_id: int) -> Optional[Dict]:
        """Получить пользователя по telegram_id"""
        users = self._read_json(self.users_file)
        return next((u for u in users if u['telegram_id'] == telegram_id), None)
    
    def get_user_by_telegram_id(self, telegram_id: int) -> Optional[Dict]:
        """Получить пользователя по telegram_id (алиас)"""
        return self.get_user(telegram_id)
    
    def update_user(self, telegram_id: int, updates: Dict):
        """Обновить поля пользователя"""
        users = self._read_json(self.users_file)
        user = next((u for u in users if u['telegram_id'] == telegram_id), None)
        
        if user:
            user.update(updates)
            user['updated_at'] = datetime.utcnow().isoformat()
            self._write_json(self.users_file, users)
            return user
        return None
    
    def verify_subscription(self, telegram_id: int):
        """Отметить подписку как проверенную"""
        users = self._read_json(self.users_file)
        user = next((u for u in users if u['telegram_id'] == telegram_id), None)
        
        if user:
            user['subscription_verified'] = True
            user['updated_at'] = datetime.utcnow().isoformat()
            self._write_json(self.users_file, users)
    
    def add_stars(self, telegram_id: int, amount: int, description: str = None):
        """Добавить звёзды"""
        users = self._read_json(self.users_file)
        user = next((u for u in users if u['telegram_id'] == telegram_id), None)
        
        if user:
            user['stars'] += amount
            user['updated_at'] = datetime.utcnow().isoformat()
            self._write_json(self.users_file, users)
            
            # Добавить транзакцию
            self._add_transaction(user['id'], 'stars_earned', amount, description or "Заработок звёзд")
    
    def subtract_stars(self, telegram_id: int, amount: int, description: str = None) -> bool:
        """Потратить звёзды"""
        users = self._read_json(self.users_file)
        user = next((u for u in users if u['telegram_id'] == telegram_id), None)
        
        if not user or user['stars'] < amount:
            return False
        
        user['stars'] -= amount
        user['updated_at'] = datetime.utcnow().isoformat()
        self._write_json(self.users_file, users)
        
        # Добавить транзакцию
        self._add_transaction(user['id'], 'stars_spent', amount, description or "Трата звёзд")
        return True
    
    def add_bears(self, telegram_id: int, amount: int, description: str = None):
        """Добавить медведей"""
        users = self._read_json(self.users_file)
        user = next((u for u in users if u['telegram_id'] == telegram_id), None)
        
        if user:
            user['bears'] += amount
            user['updated_at'] = datetime.utcnow().isoformat()
            self._write_json(self.users_file, users)
            
            # Добавить транзакцию
            self._add_transaction(user['id'], 'bears_earned', amount, description or "Заработок медведей")
    
    def get_user_balance(self, telegram_id: int) -> tuple:
        """Получить баланс пользователя"""
        user = self.get_user(telegram_id)
        if user:
            return user['stars'], user['bears']
        return None, None
    
    def _add_transaction(self, user_id: int, trans_type: str, amount: int, description: str):
        """Добавить транзакцию"""
        transactions = self._read_json(self.transactions_file)
        
        transaction = {
            'id': len(transactions) + 1,
            'user_id': user_id,
            'transaction_type': trans_type,
            'amount': amount,
            'description': description,
            'created_at': datetime.utcnow().isoformat()
        }
        
        transactions.append(transaction)
        self._write_json(self.transactions_file, transactions)
    
    def get_all_users(self) -> List[Dict]:
        """Получить всех пользователей"""
        return self._read_json(self.users_file)
    
    def request_withdrawal(self, telegram_id: int, amount: int) -> Dict:
        """Создать запрос на вывод подарков"""
        withdrawals = self._read_json(self.transactions_file)
        
        withdrawal = {
            'id': len(withdrawals) + 1,
            'user_id': telegram_id,
            'amount': amount,
            'status': 'pending',  # pending, approved, rejected
            'created_at': datetime.utcnow().isoformat()
        }
        
        withdrawals.append(withdrawal)
        self._write_json(self.transactions_file, withdrawals)
        return withdrawal
    
    def get_pending_withdrawals(self) -> List[Dict]:
        """Получить ожидающие выводы"""
        withdrawals = self._read_json(self.transactions_file)
        return [w for w in withdrawals if w.get('status') == 'pending' and w.get('user_id')]
    
    def get_user_pending_withdrawal(self, user_id: int) -> int:
        """Получить количество ожидающих выводов для пользователя"""
        withdrawals = self._read_json(self.transactions_file)
        pending = [w for w in withdrawals if w.get('user_id') == user_id and w.get('status') == 'pending']
        total = sum(w.get('amount', 0) for w in pending)
        return total
    
    def approve_withdrawal(self, user_id: int) -> bool:
        """Одобрить вывод"""
        withdrawals = self._read_json(self.transactions_file)
        
        for w in withdrawals:
            if w.get('user_id') == user_id and w.get('status') == 'pending':
                w['status'] = 'approved'
                w['approved_at'] = datetime.utcnow().isoformat()
        
        self._write_json(self.transactions_file, withdrawals)
        return True
    
    def reject_withdrawal(self, user_id: int) -> bool:
        """Отклонить вывод"""
        withdrawals = self._read_json(self.transactions_file)
        
        for w in withdrawals:
            if w.get('user_id') == user_id and w.get('status') == 'pending':
                w['status'] = 'rejected'
                w['rejected_at'] = datetime.utcnow().isoformat()
        
        self._write_json(self.transactions_file, withdrawals)
        return True
    
    def save_roulette_win(self, user_id: int, telegram_id: int, prize_name: str, ticket_id: int):
        """Сохранить выигрыш из рулетки"""
        roulette_wins = self._read_json(self.roulette_file)
        
        win_record = {
            'id': str(uuid4()),
            'user_id': user_id,
            'telegram_id': telegram_id,
            'prize_name': prize_name,
            'ticket_id': ticket_id,
            'status': 'pending',  # pending, approved, rejected
            'created_at': datetime.utcnow().isoformat(),
            'approved_at': None,
            'rejected_at': None
        }
        
        roulette_wins.append(win_record)
        self._write_json(self.roulette_file, roulette_wins)
        return win_record
    
    def get_pending_roulette_wins(self) -> List:
        """Получить все ожидающие выигрыши из рулетки (из рулетки_wins.json)"""
        roulette_wins = self._read_json(self.roulette_wins_file)
        return [w for w in roulette_wins if w.get('status') == 'pending']
    
    def approve_roulette_win(self, win_id: int) -> bool:
        """Одобрить выигрыш из рулетки"""
        roulette_wins = self._read_json(self.roulette_wins_file)
        
        for win in roulette_wins:
            if win.get('id') == win_id:
                win['status'] = 'sent'
                win['updated_at'] = datetime.utcnow().isoformat()
                self._write_json(self.roulette_wins_file, roulette_wins)
                return True
        
        return False
    
    def reject_roulette_win(self, win_id: int) -> bool:
        """Отклонить выигрыш из рулетки"""
        roulette_wins = self._read_json(self.roulette_wins_file)
        
        for win in roulette_wins:
            if win.get('id') == win_id:
                win['status'] = 'rejected'
                win['updated_at'] = datetime.utcnow().isoformat()
                self._write_json(self.roulette_wins_file, roulette_wins)
                return True
        
        return False


class PurchaseManager(JSONDatabase):
    """Менеджер покупок"""
    
    def add_purchase(self, telegram_id: int, item_id: int, item_name: str, 
                    item_price: int, purchase_type: str):
        """Добавить покупку"""
        users = self._read_json(self.users_file)
        user = next((u for u in users if u['telegram_id'] == telegram_id), None)
        
        if user:
            purchases = self._read_json(self.purchases_file)
            
            purchase = {
                'id': len(purchases) + 1,
                'user_id': user['id'],
                'item_id': item_id,
                'item_name': item_name,
                'item_price': item_price,
                'purchase_type': purchase_type,
                'created_at': datetime.utcnow().isoformat()
            }
            
            purchases.append(purchase)
            self._write_json(self.purchases_file, purchases)
    
    def get_user_purchases(self, telegram_id: int, limit: int = 10) -> List:
        """Получить историю покупок"""
        users = self._read_json(self.users_file)
        user = next((u for u in users if u['telegram_id'] == telegram_id), None)
        
        if user:
            purchases = self._read_json(self.purchases_file)
            user_purchases = [p for p in purchases if p['user_id'] == user['id']]
            return user_purchases[-limit:]
        return []


class ReferralManager(JSONDatabase):
    """Менеджер реферальной программы"""
    
    def add_referral(self, referrer_id: int, referred_user_id: int, referred_username: str = None):
        """Добавить реферала"""
        referrals = self._read_json(self.referrals_file)
        
        referral = {
            'id': len(referrals) + 1,
            'referrer_id': referrer_id,
            'referred_user_id': referred_user_id,
            'referred_username': referred_username,
            'bonus_paid': False,
            'created_at': datetime.utcnow().isoformat()
        }
        
        referrals.append(referral)
        self._write_json(self.referrals_file, referrals)
    
    def get_referral_count(self, user_id: int) -> int:
        """Получить количество рефералов"""
        referrals = self._read_json(self.referrals_file)
        return len([r for r in referrals if r['referrer_id'] == user_id and not r['bonus_paid']])
    
    def get_user_by_referral_code(self, referral_code: str) -> Optional[Dict]:
        """Получить пользователя по реф. коду"""
        users = self._read_json(self.users_file)
        return next((u for u in users if u['referral_code'] == referral_code), None)


class RouletteManager(JSONDatabase):
    """Менеджер рулетки"""
    
    def add_roulette_result(self, telegram_id: int, ticket_id: int, ticket_name: str, 
                           ticket_price: int, prize_name: str, prize_type: str, prize_value: int):
        """Добавить результат рулетки"""
        users = self._read_json(self.users_file)
        user = next((u for u in users if u['telegram_id'] == telegram_id), None)
        
        if user:
            results = self._read_json(self.roulette_file)
            
            result = {
                'id': len(results) + 1,
                'user_id': user['id'],
                'telegram_id': telegram_id,
                'username': user.get('username', ''),
                'first_name': user.get('first_name', ''),
                'ticket_id': ticket_id,
                'ticket_name': ticket_name,
                'ticket_price': ticket_price,
                'prize_name': prize_name,
                'prize_type': prize_type,
                'prize_value': prize_value,
                'created_at': datetime.utcnow().isoformat()
            }
            
            results.append(result)
            self._write_json(self.roulette_file, results)
            
            # Если это выигрыш - добавляем в отдельный файл
            if prize_type != 'no_prize':
                self.add_roulette_win(telegram_id, user['id'], result)
    
    def add_roulette_win(self, telegram_id: int, user_id: int, result: dict):
        """Добавить выигрыш в отдельный файл"""
        wins = self._read_json(self.roulette_wins_file)
        
        win = {
            'id': len(wins) + 1,
            'user_id': user_id,
            'telegram_id': telegram_id,
            'username': result.get('username', ''),
            'first_name': result.get('first_name', ''),
            'ticket_name': result.get('ticket_name', ''),
            'ticket_price': result.get('ticket_price', 0),
            'prize_name': result.get('prize_name', ''),
            'prize_type': result.get('prize_type', ''),
            'prize_value': result.get('prize_value', 0),
            'created_at': result.get('created_at', ''),
            'status': 'pending'  # pending, sent, rejected
        }
        
        wins.append(win)
        self._write_json(self.roulette_wins_file, wins)
        return win
    
    def get_pending_wins(self) -> List:
        """Получить все ожидающие выигрыши для отправки"""
        wins = self._read_json(self.roulette_wins_file)
        return [w for w in wins if w.get('status') == 'pending']
    
    def mark_win_sent(self, win_id: int) -> bool:
        """Отметить выигрыш как отправленный"""
        wins = self._read_json(self.roulette_wins_file)
        
        for win in wins:
            if win.get('id') == win_id:
                win['status'] = 'sent'
                self._write_json(self.roulette_wins_file, wins)
                return True
        
        return False


# Создать глобальный экземпляр база данных
db = JSONDatabase()
user_manager = UserManager()
purchase_manager = PurchaseManager()
referral_manager = ReferralManager()
roulette_manager = RouletteManager()
