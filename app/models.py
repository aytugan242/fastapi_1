import datetime

from config import PG_DSN

from sqlalchemy import Integer, Float, DateTime, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(
    PG_DSN,
)

Session = async_sessionmaker(bind=engine, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    pass


class Advertisement(Base):
    __tablename__ = 'advertisement'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    author: Mapped[str] = mapped_column(String(100))
    price: Mapped[float] = mapped_column(Float)
    date_of_creation: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )

    @property
    def dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'author': self.author,
            'price': self.price,
            'date_of_creation': self.date_of_creation.isoformat()
        }