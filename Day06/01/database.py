from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine, Column, String, Integer


DATABASE_URL = 'sqlite:///./test.db'

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

class UserAct(Base):
    __tablename__ = 'user_act'

    id = Column(Integer,primary_key=True, index=True)
    username = Column(String, index=True)
    action = Column(String)
Base.metadata.create_all(bind=engine)

def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()