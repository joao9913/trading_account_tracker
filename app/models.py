from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Numeric, String, ForeignKey, Date, DateTime, UniqueConstraint
from app.database import Base

class Account(Base):
    __tablename__ = "account"

    id = Column(Integer, primary_key=True) #MT5 Account number
    owner = Column(String, nullable=False)
    starting_balance = Column(Numeric(12, 2), nullable=False)
    current_balance = Column(Numeric(12, 2), nullable=False)
    profit_target = Column(Numeric(12, 2), nullable=False)
    max_drawdown = Column(Numeric(12, 2), nullable=False)
    starting_date = Column(Date, nullable=False)
    ending_date = Column(Date)
    account_status = Column(String, nullable=False)

    strategy_id = Column(Integer, ForeignKey("strategy.id"), nullable=False)
    strategy = relationship("Strategy", back_populates="accounts")
    trades = relationship("Trade", back_populates="account", cascade="all, delete-orphan")

class Strategy(Base):
    __tablename__ = "strategy"

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False, unique=True)
    
    accounts = relationship("Account", back_populates="strategy")
    
class Trade(Base):
    __tablename__ = "trade"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("account.id"), nullable=False)

    symbol = Column(String, nullable=False)
    pnl = Column(Numeric(12, 2))
    open_datetime = Column(DateTime, nullable=False)
    close_datetime = Column(DateTime)
    ticket_id = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint("ticket_id", "account_id", name="unique_ticket_per_account"),
    )

    account = relationship("Account", back_populates="trades")