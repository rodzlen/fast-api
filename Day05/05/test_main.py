from http.client import responses

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from database import get_db, Product, Base

from main import app, ProductRequests

client = TestClient(app)

TEST_DATABASE_URL = 'sqlite:///./test_db.sqlite'
engine = create_engine(TEST_DATABASE_URL, connect_args={'check_same_thread': False})

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope='function')
def setup_test_data():
    Base.metadata.drop_all(bind= engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    db.add_all([
        Product(name='a',price=20),
        Product(name='q',price=13),
        ]
    )
    db.commit()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_get_products():
    response = client.get('/products')
    assert response.status_code == 200

def test_post_product():
    response = client.post('/products', json={'name':"zzxc","price":120})
    assert response.status_code == 200
    assert response.json() == {'id':7, 'name':"zzxc","price":120}
def test_get_product():
    response = client.get('/products/1')
    assert response.status_code ==200
    assert response.json() == {'id':1,'name':'zzxc', "price":120}