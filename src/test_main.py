import json
from fastapi.testclient import TestClient
from fastapi import status
import pytest

from main import app

client = TestClient(app)


def test_get_public():
    response = client.get("/api/v1/references/get_public")
    assert response is not None
    assert response.status_code == 200

def test_ping():
    response = client.get('/ping')
    assert response is not None
    assert response.status_code == 200
    assert response.json() == "Database is working"

# Честно говоря не знаю, как реализовывать тетсты для OAuth2PasswordRequestForm. Сами методы можно просмотреть в Swagger