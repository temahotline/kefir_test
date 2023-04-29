from sqlalchemy import Column, String, Date, Integer, Boolean

from src.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True,)
    first_name = Column(String, nullable=False,)
    last_name = Column(String, nullable=False,)
    other_name = Column(String, nullable=True,)
    email = Column(String, nullable=False, unique=True,)
    phone = Column(String, nullable=True, unique=True,)
    birthday = Column(Date, nullable=True,)
    city = Column(Integer, nullable=True,)
    additional_info = Column(String, nullable=True,)
    is_admin = Column(Boolean, nullable=False,)
    is_active = Column(Boolean, nullable=False, default=True)
    hashed_password = Column(String, nullable=False,)


class City(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True, index=True,)
    name = Column(String, nullable=False, unique=True,)
