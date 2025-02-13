from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,String, Integer, select


app = FastAPI()

DATABASE_URL = 'sqlite+aiosqlite:///./test.db'

async_engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

class Animal(Base):
    __tablename__ = 'animals'

    id = Column(Integer, primary_key=True, index=True)
    name= Column(String, index=True)
    species = Column(String,index=True)
    age = Column(Integer, index=True)

# Dependency 비동기 세션 생성
async def get_db():
    async  with AsyncSessionLocal() as session:
        yield session

@app.get('/animals/')
async def get_list(db:AsyncSessionLocal=Depends(get_db)):
    result = await db.execute(select(Animal))
    animals = result.scalars().all()
    return animals

@app.get('/animals/by-species')
async def get_speices(species:str, db:AsyncSessionLocal=Depends(get_db)):
    result = await db.execute(select(Animal).filter(Animal.species==species))
    animals = result.scalars().all()
    return animals

@app.get('/animals/by-min-age')
async def get_min_age(min_age:int, db:AsyncSessionLocal=Depends(get_db)):
    result = await db.execute(select(Animal).filter(Animal.age >= min_age))
    animals = result.scalars().all()
    return animals

@app.get('/animals/search-by-name')
async def get_by_name(name:str, db:AsyncSessionLocal=Depends(get_db)):
    result = await db.execute(select(Animal).filter(Animal.name.ilike(f'%{name}%')))
    animals = result.scalars().all()
    return animals

@app.get('/animals/sorted-by-age')
async def get_animals_sorted(db: AsyncSessionLocal = Depends(get_db)):
    result = await db.execute(select(Animal).order_by(Animal.age))
    animals = result.scalars().all()
    return animals

@app.get('/animals/{animal_id}')
async def get_animal_by_id(animal_id : int, db: AsyncSessionLocal = Depends(get_db)):
    animal = await db.get(Animal, animal_id)
    if not animal:
        return HTTPException(status_code=400, detail='Not found data')
    return animal