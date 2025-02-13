import json, asyncio
from contextlib import asynccontextmanager

from jose import jwt
from fastapi import FastAPI, Depends, HTTPException
from passlib.context import CryptContext
from datetime import datetime, timedelta
from pydantic import BaseModel
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import Column, String, Integer, Boolean, DATETIME,select


DATABASE_URL = 'mysql+aiomysql://root:1234@127.0.0.1:3306/fast_test'
async_engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(bind=async_engine, class_= AsyncSession, expire_on_commit=False)
Base = declarative_base()

async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(lambda conn: Base.metadata.create_all(conn))

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


class Timestamp(Base):
    __abstract__ = True

    joined_at = Column(DATETIME, default=datetime.utcnow())
    modified_at = Column(DATETIME, default=datetime.utcnow(), onupdate=datetime.utcnow())

class User(Timestamp):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), unique=True, index=True)
    name = Column(String(30), nullable=False ,index=True)
    password = Column(String(255), nullable=False, index=True)
    is_admin = Column(Boolean, default=False, index=True)

class UserRegister(BaseModel):
    name : str
    password : str
    email : str

class UserLogin(BaseModel):
    email : str
    password : str

class Token(BaseModel):
    access_token:str
    token_type : str

async def create_user(user:UserRegister):
    async with AsyncSessionLocal() as session:
        stmt = select(User).where(User.email == user.email)
        result = await session.execute(stmt)

        existing_user = result.scalars().first()

        if existing_user:
            raise HTTPException(status_code=400, detail='이미 존재하는 이메일입니다.')

        hashed_password = hash_password(user.password)

        new_user = User(name= user.name,password=hashed_password, email= user.email)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user



with open(".secret.json", "r") as f:
    secret_data = json.load(f)

SECRET_KEY = secret_data['SECRET_KEY']
ACCESS_TOKEN_EXPIRE_MINUTES = secret_data['ACCESS_TOKEN_EXPIRE_MINUTES']
ALGORITHM = secret_data['ALGORITHM']


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# 비밀번호 해시화
def hash_password(password: str):
    return pwd_context.hash(password)

# 비밀번호 검증
def verified_password(plain_password:str , hashed_password:str):
    return pwd_context.verify(plain_password,hashed_password)

def create_access_token(data : dict):
    # 깊은 복사를 위해 copy()사용
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,key=SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Initializing database...")
    await init_db()  # ✅ 애플리케이션이 시작될 때 DB 초기화
    yield
    print("Shutting down application...")

app = FastAPI(lifespan=lifespan)


@app.post('/register')
async def register(user : UserRegister):
    created_user = await create_user(user)
    return {"success": True, "name":created_user.name}

@app.post('/login')
async def login(user:UserLogin, db:AsyncSession =Depends(get_db)):
    result = await db.execute(select(User).filter(User.email == user.email))
    db_user = result.scalars().first()
    if not db_user or not verified_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail='없는 이메일 이거나 비밀번호입니다.')
    access_token = create_access_token(data={"sub":user.email})
    return {"access_token" : access_token, "token_typ": "bearer"}