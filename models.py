import datetime
import os

from sqlalchemy import create_engine, Integer, String, DateTime, func
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
import atexit


POSTGRES_USER = os.getenv('POSTGRES_USER', 'user')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', '1234')
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5431")
POSTGRES_DB = os.getenv("POSTGRES_DB", "test_db")

PG_DSN = (f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}')

engine = create_engine(PG_DSN)

Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):

    @property
    def id_dict(self):
        return {'id': self.id}

class Ann(Base):
    __tablename__ = 'announcement'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    date_of_creation: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    owner:Mapped[str] = mapped_column(String, nullable=False)


    @property
    def dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'date_of_creation': self.date_of_creation.isoformat(),
            'owner': self.owner

        }


Base.metadata.create_all(bind=engine)
atexit.register(engine.dispose)



