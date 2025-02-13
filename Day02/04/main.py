import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker,declarative_base
from sqlalchemy import Column, Integer, String, text

DATABASE_URL = 'sqlite+aiosqlite:///:memory:'

# async engine설정
async_engine = create_async_engine(
    DATABASE_URL,
    echo =True # 쿼리 log 출력
)
# Async Session 설정
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_= AsyncSession,
    expire_on_commit=False
)
# Base 설정
Base = declarative_base()

# 모델
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

# DB초기화 함수
async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    async with AsyncSessionLocal()as session:
        yield session

# CRUD 함수
#1. Create
async def create_user(name: str, email:str):
    async with AsyncSessionLocal() as session:
        new_user = User(name=name, email=email)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user

async def get_all_users():
    async with AsyncSessionLocal() as session:
        result = await session.execute(text("SELECT * FROM users"))
        users= result.fetchall()
        return users

async def get_user_by_email(email:str):
    async with  AsyncSessionLocal() as session:
        result = await session.execute(
            text("SELECT * FROM users WHERE email = :email"),
            {"email":email})
        user = result.fetchone()
        return user

async def update_user( user_id:int, name:str, email:str):
    async with AsyncSessionLocal() as session:
        user = await session.get(User, user_id)
        if not user:
            return None

        user.name = name
        user.email = email
        await session.commit()
        await session.refresh(user)
        return user

async def delete_user(user_id:int):
    async with AsyncSessionLocal() as session:
        existing_user = await session.get(User,user_id)
        if not existing_user:
            return None

        session.delete(existing_user)
        session.commit()
        return user_id

if __name__=="__main__":
    async def main():
        await init_db()



    asyncio.run(main())