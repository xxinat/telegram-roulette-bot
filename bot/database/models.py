"""
Модели БД для хранения данных бота
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    """Модель пользователя"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False, index=True)
    username = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255))
    
    # Баланс
    stars = Column(Integer, default=100)
    bears = Column(Integer, default=0)
    
    # Реферальная система
    referral_code = Column(String(50), unique=True, nullable=False)
    referred_by = Column(String(50), nullable=True)  # Реферальный код того, кто пригласил
    referral_count = Column(Integer, default=0)
    
    # Проверка подписки
    subscription_verified = Column(Boolean, default=False)
    
    # Даты
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Связи
    purchases = relationship("Purchase", back_populates="user")
    referrals = relationship("Referral", back_populates="referrer")
    transactions = relationship("Transaction", back_populates="user")
    
    def __repr__(self):
        return f"<User(telegram_id={self.telegram_id}, username={self.username}, stars={self.stars})>"


class Purchase(Base):
    """Модель покупок"""
    __tablename__ = "purchases"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    item_id = Column(Integer, nullable=False)
    item_name = Column(String(255), nullable=False)
    item_price = Column(Integer, nullable=False)
    purchase_type = Column(String(50), nullable=False)  # "shop", "roulette"
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Связь
    user = relationship("User", back_populates="purchases")
    
    def __repr__(self):
        return f"<Purchase(user_id={self.user_id}, item_name={self.item_name}, price={self.item_price})>"


class Transaction(Base):
    """Модель транзакций (доход/расход)"""
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Тип: stars_earned, stars_spent, bears_earned, bears_spent
    transaction_type = Column(String(50), nullable=False)
    
    # Сумма
    amount = Column(Integer, nullable=False)
    
    # Описание
    description = Column(String(255), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Связь
    user = relationship("User", back_populates="transactions")
    
    def __repr__(self):
        return f"<Transaction(user_id={self.user_id}, type={self.transaction_type}, amount={self.amount})>"


class Referral(Base):
    """Модель реферальной программы"""
    __tablename__ = "referrals"
    
    id = Column(Integer, primary_key=True)
    referrer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    referred_user_id = Column(Integer, nullable=False)
    referred_username = Column(String(255), nullable=True)
    
    # Бонус выплачен?
    bonus_paid = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Связь
    referrer = relationship("User", back_populates="referrals")
    
    def __repr__(self):
        return f"<Referral(referrer_id={self.referrer_id}, referred_user_id={self.referred_user_id})>"


class RouletteResult(Base):
    """Модель результатов рулетки"""
    __tablename__ = "roulette_results"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    ticket_id = Column(Integer, nullable=False)
    ticket_name = Column(String(255), nullable=False)
    ticket_price = Column(Integer, nullable=False)
    
    # Результат
    prize_name = Column(String(255), nullable=False)
    prize_type = Column(String(50), nullable=False)
    prize_value = Column(Integer, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<RouletteResult(user_id={self.user_id}, prize={self.prize_name})>"
