from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class Book(Base):
    __tablename__ = "books"

    id     = Column(Integer, primary_key=True, index=True)
    title  = Column(String,  nullable=False)
    author = Column(String,  nullable=False)
    status = Column(String,  default="want_to_read")
    rating = Column(Integer, nullable=True)