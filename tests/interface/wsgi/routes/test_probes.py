from fastapi.testclient import TestClient

from src.interface.wsgi.app import app

client = TestClient(app)


def test_probe_health_check():
    response = client.get("/")
    assert response.status_code == 200
