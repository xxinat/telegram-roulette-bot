"""
Утилиты для работы с БД
"""

import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from database.models import Base, User, Purchase, Transaction, Referral, RouletteResult
from config import DATABASE_URL, STARTING_STARS


# Создание движка БД
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Создание сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Инициализация БД"""
    Base.metadata.create_all(bind=engine)


def get_db() -> Session:
    """Получить сессию БД"""
    return SessionLocal()


def generate_referral_code() -> str:
    """Генерация уникального реферального кода"""
    return str(uuid.uuid4())[:8].upper()


class UserManager:
    """Менеджер для работы с пользователями"""
    
    @staticmethod
    def get_or_create_user(telegram_id: int, username: str = None, first_name: str = None, last_name: str = None) -> User:
        """Получить или создать пользователя"""
        db = get_db()
        try:
            user = db.query(User).filter(User.telegram_id == telegram_id).first()
            
            if user:
                # Обновить информацию
                if username:
                    user.username = username
                if first_name:
                    user.first_name = first_name
                if last_name:
                    user.last_name = last_name
                db.commit()
                return user
            
            # Создать нового пользователя
            referral_code = generate_referral_code()
            new_user = User(
                telegram_id=telegram_id,
                username=username,
                first_name=first_name,
                last_name=last_name,
                stars=STARTING_STARS,
                referral_code=referral_code
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return new_user
        finally:
            db.close()
    
    @staticmethod
    def get_user(telegram_id: int) -> User:
        """Получить пользователя по telegram_id"""
        db = get_db()
        try:
            return db.query(User).filter(User.telegram_id == telegram_id).first()
        finally:
            db.close()
    
    @staticmethod
    def verify_subscription(telegram_id: int):
        """Отметить подписку как проверенную"""
        db = get_db()
        try:
            user = db.query(User).filter(User.telegram_id == telegram_id).first()
            if user:
                user.subscription_verified = True
                db.commit()
        finally:
            db.close()
    
    @staticmethod
    def add_stars(telegram_id: int, amount: int, description: str = None):
        """Добавить звёзды пользователю"""
        db = get_db()
        try:
            user = db.query(User).filter(User.telegram_id == telegram_id).first()
            if user:
                user.stars += amount
                db.commit()
                
                # Добавить транзакцию
                transaction = Transaction(
                    user_id=user.id,
                    transaction_type="stars_earned",
                    amount=amount,
                    description=description or "Заработок звёзд"
                )
                db.add(transaction)
                db.commit()
        finally:
            db.close()
    
    @staticmethod
    def subtract_stars(telegram_id: int, amount: int, description: str = None) -> bool:
        """Потратить звёзды. Возвращает True если успешно"""
        db = get_db()
        try:
            user = db.query(User).filter(User.telegram_id == telegram_id).first()
            if not user:
                return False
            
            if user.stars < amount:
                return False
            
            user.stars -= amount
            db.commit()
            
            # Добавить транзакцию
            transaction = Transaction(
                user_id=user.id,
                transaction_type="stars_spent",
                amount=amount,
                description=description or "Трата звёзд"
            )
            db.add(transaction)
            db.commit()
            return True
        finally:
            db.close()
    
    @staticmethod
    def add_bears(telegram_id: int, amount: int, description: str = None):
        """Добавить медведей пользователю"""
        db = get_db()
        try:
            user = db.query(User).filter(User.telegram_id == telegram_id).first()
            if user:
                user.bears += amount
                db.commit()
                
                # Добавить транзакцию
                transaction = Transaction(
                    user_id=user.id,
                    transaction_type="bears_earned",
                    amount=amount,
                    description=description or "Заработок медведей"
                )
                db.add(transaction)
                db.commit()
        finally:
            db.close()
    
    @staticmethod
    def get_user_balance(telegram_id: int) -> tuple:
        """Получить баланс пользователя (звёзды, медведи)"""
        db = get_db()
        try:
            user = db.query(User).filter(User.telegram_id == telegram_id).first()
            if user:
                return user.stars, user.bears
            return None, None
        finally:
            db.close()


class PurchaseManager:
    """Менеджер для работы с покупками"""
    
    @staticmethod
    def add_purchase(telegram_id: int, item_id: int, item_name: str, item_price: int, purchase_type: str):
        """Добавить покупку"""
        db = get_db()
        try:
            user = db.query(User).filter(User.telegram_id == telegram_id).first()
            if user:
                purchase = Purchase(
                    user_id=user.id,
                    item_id=item_id,
                    item_name=item_name,
                    item_price=item_price,
                    purchase_type=purchase_type
                )
                db.add(purchase)
                db.commit()
        finally:
            db.close()
    
    @staticmethod
    def get_user_purchases(telegram_id: int, limit: int = 10) -> list:
        """Получить историю покупок пользователя"""
        db = get_db()
        try:
            user = db.query(User).filter(User.telegram_id == telegram_id).first()
            if user:
                return db.query(Purchase).filter(Purchase.user_id == user.id).order_by(
                    Purchase.created_at.desc()
                ).limit(limit).all()
            return []
        finally:
            db.close()


class ReferralManager:
    """Менеджер для работы с реферальной программой"""
    
    @staticmethod
    def add_referral(referrer_id: int, referred_user_id: int, referred_username: str = None):
        """Добавить нового приглашённого пользователя"""
        db = get_db()
        try:
            referral = Referral(
                referrer_id=referrer_id,
                referred_user_id=referred_user_id,
                referred_username=referred_username
            )
            db.add(referral)
            db.commit()
        finally:
            db.close()
    
    @staticmethod
    def get_referral_count(user_id: int) -> int:
        """Получить количество приглашённых"""
        db = get_db()
        try:
            count = db.query(Referral).filter(Referral.referrer_id == user_id, Referral.bonus_paid == False).count()
            return count
        finally:
            db.close()
    
    @staticmethod
    def get_user_by_referral_code(referral_code: str) -> User:
        """Получить пользователя по реферальному коду"""
        db = get_db()
        try:
            return db.query(User).filter(User.referral_code == referral_code).first()
        finally:
            db.close()


class RouletteManager:
    """Менеджер для работы с рулеткой"""
    
    @staticmethod
    def add_roulette_result(telegram_id: int, ticket_id: int, ticket_name: str, ticket_price: int, 
                           prize_name: str, prize_type: str, prize_value: int):
        """Добавить результат рулетки"""
        db = get_db()
        try:
            user = db.query(User).filter(User.telegram_id == telegram_id).first()
            if user:
                result = RouletteResult(
                    user_id=user.id,
                    ticket_id=ticket_id,
                    ticket_name=ticket_name,
                    ticket_price=ticket_price,
                    prize_name=prize_name,
                    prize_type=prize_type,
                    prize_value=prize_value
                )
                db.add(result)
                db.commit()
        finally:
            db.close()
