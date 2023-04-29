from datetime import date
from typing import Union, List

from sqlalchemy import update, select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.models import User, City


class UserDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(
            self,
            first_name: str,
            last_name: str,
            other_name: str,
            email: str,
            phone: str,
            birthday: date,
            city: int,
            additional_info: str,
            is_admin: bool,
            hashed_password: str,
    ) -> User:
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            other_name=other_name,
            email=email,
            phone=phone,
            birthday=birthday,
            city=city,
            additional_info=additional_info,
            is_admin=is_admin,
            hashed_password=hashed_password,
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user

    async def delete_user(self, user_id: int) -> Union[bool, None]:
        query = (
            update(User)
            .where(User.id == user_id)
            .values(is_active=False)
            .returning(User.id)
        )
        res = await self.db_session.execute(query)

        if res.rowcount == 1:
            return True

    async def update_user(self, user_id: int, **kwargs) -> Union[User, None]:
        query = (
            update(User)
            .where(and_(User.id == user_id, User.is_active == True))
            .values(kwargs)
            .returning(User)
        )
        res = await self.db_session.execute(query)
        user = res.fetchone()
        if user is not None:
            return user[0]

    async def get_users(self, page: int, size: int,) -> list[User]:
        offset = (page - 1) * size
        query = (
            select(User)
            .where(User.is_active == True)
            .offset(offset)
            .limit(size)
        )
        res = await self.db_session.execute(query)
        users = res.fetchall()
        return [user for user, in users]

    async def get_user_by_id(self, user_id: int) -> Union[User, None]:
        query = select(User).where(User.id == user_id)
        res = await self.db_session.execute(query)
        user = res.fetchone()
        if user is not None:
            return user[0]

    async def get_total_users_count(self) -> int:
        query = select(func.count()).select_from(User).where(User.is_active == True)
        res = await self.db_session.execute(query)
        return res.scalar()

    async def get_user_by_email(self, email: str) -> Union[User, None]:
        query = select(User).where(User.email == email)
        res = await self.db_session.execute(query)
        user = res.fetchone()
        if user is not None:
            return user[0]
        return None

    async def get_user_by_phone(self, phone: str) -> Union[User, None]:
        query = select(User).where(User.phone == phone)
        res = await self.db_session.execute(query)
        user = res.fetchone()
        if user is not None:
            return user[0]
        return None


class CityDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_city(self, name: str) -> City:
        new_city = City(
            name=name,
        )
        self.db_session.add(new_city)
        await self.db_session.flush()
        return new_city

    async def get_cities(self) -> List[City]:
        query = select(City)
        res = await self.db_session.execute(query)
        cities = res.fetchall()
        return [city for city, in cities]
