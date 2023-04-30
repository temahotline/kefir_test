import asyncio

from getpass import getpass

from src.database import async_session
from src.security import Hasher
from src.users.dals import UserDAL


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
            other_name=None,  # Заполните другие поля для админа здесь
            email=email,
            phone=None,
            birthday=None,
            city=None,
            additional_info=None,
            is_admin=True,
            hashed_password=hashed_password,
        )
        await session.commit()
        await session.refresh(admin)
        print(f"Admin user created with ID: {admin.id}")


if __name__ == "__main__":
    asyncio.run(create_admin())
