from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, Numeric, String, ForeignKey, Date, DateTime
from app.database import Base

class Account(Base):
    __tablename__ = "account"

    id = Column(Integer, primary_key=True)
    owner = Column(String, nullable=False)
    starting_balance = Column(Numeric(12, 2), nullable=False)
    current_balance = Column(Numeric(12, 2), nullable=False)
    profit_target = Column(Numeric(12, 2), nullable=False)
    max_drawdown = Column(Numeric(12, 2), nullable=False)
    starting_date = Column(Date, nullable=False)

    strategies = relationship("Strategy", back_populates="account", cascade="all, delete-orphan")

class Strategy(Base):
    __tablename__ = "strategy"

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("account.id"),nullable=False)
    name = Column(String(30), nullable=False)

    account = relationship("Account", back_populates="strategies")
    trades = relationship("Trade", back_populates="strategy", cascade="all, delete-orphan")
    
class Trade(Base):
    __tablename__ = "trade"

    id = Column(Integer, primary_key=True)
    strategy_id = Column(Integer, ForeignKey("strategy.id"), nullable=False)
    symbol = Column(String(10), nullable=False)
    pnl = Column(Numeric(12, 2), nullable=False)
    open_datetime = Column(DateTime, nullable=False)
    close_datetime = Column(DateTime)

    strategy = relationship("Strategy", back_populates="trades")