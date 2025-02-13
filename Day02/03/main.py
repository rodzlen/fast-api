from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import  create_engine, Column, String, Integer, between, desc
from pydantic import BaseModel




# DB url 설정
DATA_BASE_URL = 'sqlite:///./test.db'


# SQLAlchemy 엔진 및 세션 설정
engine = create_engine(DATA_BASE_URL, connect_args={'check_same_thread': False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#sqlAlchemy 기본 베이스 생성
Base = declarative_base()

app = FastAPI()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)


Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# 모든유저 이름만 반환
@app.get('/users/')
def read_users(skip : int =0, limit:int=10, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return [{"name": user.name} for user in users]


# 특정 이름 포함된 유저
@app.get('/user/name-find')
def get_user_by_name(username : str='', db:Session=Depends(get_db)):
    users = db.query(User).filter(User.name.ilike(f'%{username}%')).all()
    return {"users":{"user": [user for user in users]}}

#user_id 특정 반환
@app.get('/users/{user_id}')
def read_user(user_id:int , db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user
#email 특정 반환
@app.get('/users/search/email/{email}')
def get_eamil(email:str , db : Session = Depends(get_db)):
    user = db.query(User).filter(User.email== email).first()
    return user

# id 범위로 검색
@app.get('/users/search/id')
def get_id(skip:int=1, limit:int=10, db:Session = Depends(get_db)):
    users = db.query(User).filter(User.id.between(skip,limit)).all()
    return {"users":{"user": [user for user in users]}}

# 이름순 정렬
@app.get('/users/order/')
def get_list_order(db:Session=Depends(get_db)):
    users = db.query(User).order_by('name').all()
    return {"users":{"user": [user for user in users]}}

# id 역순
@app.get('/users/reverse-id/')
def get_list_order(db:Session=Depends(get_db)):
    users = db.query(User).order_by(desc('id')).all()
    return {"users":{"user": [user for user in users]}}

# 사용자 수 반혼
@app.get('/users/count/')
def get_count(db:Session=Depends(get_db)):
    user_count = db.query(User).count()
    return {"count":user_count}

#특정 id 이상인 사용자 반환
@app.get('/users')
def get_user_ge(num:int=1, db: Session = Depends(get_db)):
    users = db.query(User).filter(User.id>=num).all()
    return {"users": {"user": [user for user in users]}}

class CreateUser(BaseModel):
    name: str
    email : str


# 데이터 생성
@app.post('/users/')
def create_user(user:CreateUser, db:Session = Depends(get_db), ):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="이미 존재하는 이메일입니다")
    new_user = User(name=user.name, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user) # 새로 추가된 데이터 반환을 위한 refresh

    return new_user