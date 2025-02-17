from main import multi, app

from fastapi.testclient import TestClient

client = TestClient(app)


def test_multi():
    response = client.get('/math/multiply')
    result = multi(1,123)
    assert result == {'result':123}
    assert multi(10,10) == {'result':100}

def test_add_zero():
    response = client.get('/math/multiply')

    result = multi(1,0)
    assert result == {'result': 0}

def test_add_nagative():
    response = client.get('/math/multiply')
    result = multi(1,-1)
    assert result == {'result': -1}