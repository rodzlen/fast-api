import pytest, time
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from main import app, ItemCreate
from database import Item, get_db, Base, engine, SessionLocal

client = TestClient(app)

@patch('main.get_db')
def test_get_item_with_mock(mock_get_db):
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = Item(id=1, name="Mock Item", price=5000)

    mock_get_db.return_value = mock_db
    app.dependency_overrides[get_db] = lambda : mock_db

    response = client.get("/items/1")

    assert response.status_code == 200
    assert response.json()['name'] == "Mock Item"

    app.dependency_overrides.clear()

@pytest.fixture(scope='module')
def test_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db =SessionLocal()
    db.add(Item(id=1, name="Laptop", price=1500))
    db.commit()
    yield db
    db.close()

@pytest.mark.parametrize("item_data, expected_status",[
    (ItemCreate(id=2, name='Phone', price=800).model_dump(),200),
(ItemCreate(id=3, name='Tablet', price=-100).model_dump(),200)
])
def test_create_item(item_data, expected_status):
    response = client.post('/items/', json=item_data)
    assert response.status_code == expected_status


@pytest.mark.parametrize("item_id, apply_discount, expected_price", [
    (1, False, 1500),
    (1, True, 1200),  # 20% 할인 적용
])
def test_get_item_discount(item_id, apply_discount, expected_price, test_db):
    response = client.get(f"/items/{item_id}?apply_discount={apply_discount}")
    assert response.status_code == 200
    assert response.json()["price"] == expected_price

# 성능 측정 테스트
def test_performance():
    start_time = time.time()
    response = client.get("/items/1")
    end_time = time.time()
    assert response.status_code == 200
    print(f"\nAPI 실행 시간: {end_time - start_time:.5f}초")