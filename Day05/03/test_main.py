from main import app, get_div
from fastapi.testclient import TestClient

client = TestClient(app)
#  0 으로 나눌 시
def test_check_zero():
    response =client.post('/math/devide', params={"a":10, "b":0})
    assert response.status_code == 400
    assert response.json() == {"detail": "0으로 나눌 수 없습니다"}

#
def test_check():
    response =client.post('/math/devide', params={"a":10, "b":1})
    assert response.status_code == 200
    assert response.json() == 10

def test_check_nagative():
    response =client.post('/math/devide', params={"a":10, "b":-1})
    assert response.status_code == 200
    assert response.json() == -10