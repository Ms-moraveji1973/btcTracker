from sqlalchemy.orm import  Mapped , mapped_column
from sqlalchemy import String, Integer , DateTime
from datetime import datetime
from database import Base


class Crypto(Base):
    __tablename__ = 'prices'
    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    crypto_symbol: Mapped[str] = mapped_column(String(50))
    crypto_price: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime)