from sqlalchemy.ext.asyncio import AsyncSession
from models.base import Base
from db.database import engine

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    import asyncio
    asyncio.run(init_db()) 