import asyncio

from src.database import async_session
from src.users.dals import CityDAL


async def create_city():
    city_name = input("Enter city name: ")

    async with async_session() as session:
        city_dal = CityDAL(session)
        city = await city_dal.create_city(name=city_name)
        await session.commit()
        await session.refresh(city)
        print(f"City created with ID: {city.id}")

if __name__ == "__main__":
    asyncio.run(create_city())
