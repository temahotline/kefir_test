import os
import asyncio
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from getpass import getpass

from src.users.dals import UserDAL
from src.users.utils import Hasher

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_async_engine(DATABASE_URL)
Base = declarative_base()
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def create_admin():
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    email = input("Enter email: ")
    password = getpass("Enter password: ")
    hashed_password = Hasher.get_password_hash(password)

    async with async_session() as session:
        user_dal = UserDAL(session)
        admin = await user_dal.create_user(
            first_name=first_name,
            last_name=last_name,
            other_name="",  # Заполните другие поля для админа здесь
            email=email,
            phone="",
            birthday=None,
            city=None,
            additional_info="",
            is_admin=True,
            hashed_password=hashed_password,
        )
        await session.commit()
        await session.refresh(admin)
        print(f"Admin user created with ID: {admin.id}")

if __name__ == "__main__":
    asyncio.run(create_admin())
