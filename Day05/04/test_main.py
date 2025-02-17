from main import app, get_data
from fastapi.testclient import TestClient

client = TestClient(app)
TEST_DATA = {
    1:{'id': 1, 'name':"Laptop", "price":1200},
    2: {"id":2, "name":"Phone", "price":800},
    3: {"id":3, "name":"Tablet", "price":600},
}

def override_get_data():
    return TEST_DATA
app.dependency_overrides[get_data] = override_get_data



def test_get_item():
    response = client.post('/items/1')
    assert response.status_code == 200
    assert response.json() =={'id': 1, 'name':"Laptop", "price":1200}

def test_get_items():
    response = client.post('/items')
    assert response.status_code == 200
    assert response.json() =={
    "1":{'id': 1, 'name':"Laptop", "price":1200},
    "2": {"id":2, "name":"Phone", "price":800},
    "3": {"id":3, "name":"Tablet", "price":600},
}
