from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, Double, String, ForeignKey
from app.database import Base

class Trader(Base):
    __tablename__ = "trader"

    id = Column(Integer, primary_key=True)

    strategies = relationship("Strategy", back_populates="trader", cascade="all, delete-orphan")

class Strategy(Base):
    __tablename__ = "strategy"

    id = Column(Integer, primary_key=True)
    trader_id = Column(Integer, ForeignKey("trader.id"),nullable=False)

    trader = relationship("Trader", back_populates="strategies")
    trades = relationship("Trade", back_populates="strategy", cascade="all, delete-orphan")
    
class Trade(Base):
    __tablename__ = "trade"

    id = Column(Integer, primary_key=True)
    strategy_id = Column(Integer, ForeignKey("strategy.id"), nullable=False)

    strategy = relationship("Strategy", back_populates="trades")