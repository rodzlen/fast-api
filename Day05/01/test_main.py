from main import add, sub, app

from fastapi.testclient import TestClient

client = TestClient(app)


def test_add():
    response = client.get('/add')
    result = add(1,123)
    assert result == {'add':124}

def test_add_zero():
    response = client.get('/add')
    result = add(1,0)
    assert result == {'add': 1}

def test_add_nagative():
    response = client.get('/add')
    result = add(1,-1)
    assert result == {'add': 0}

def test_sub():
    response = client.get('/sub')

    result = sub(-1,1)
    assert result == {'sub': -2}

def test_sub_big():
    response = client.get('/sub')

    result = sub(-10000000000000,1)
    assert result == {'sub': -10000000000001}