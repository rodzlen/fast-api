from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite 메모리 설정
DATABASE_URL = 'sqlite:///:memory:'
engine = create_engine(DATABASE_URL, echo=True)

# ORM 설정
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#모델 정의
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

# 테이블 생성
Base.metadata.create_all(bind=engine)

# 데이터 작업
session = SessionLocal()
new_user = User(name="John Doe13")
session.add(new_user)
session.commit()

users= session.query(User).all()
for user in users:
    print(user.name)
