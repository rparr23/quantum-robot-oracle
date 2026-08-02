import pytest

from app import create_app


@pytest.fixture()
def client():
    app = create_app()
    app.config.update(TESTING=True)
    return app.test_client()


def test_home_and_health(client):
    assert client.get("/").status_code == 200
    assert client.get("/api/health").json == {"simulator": "qiskit-aer", "status": "ok"}


def test_oracle_api(client):
    response = client.post("/api/oracle", json={"question": "Ship it?", "shots": 128})
    assert response.status_code == 200
    assert sum(response.json["counts"].values()) == 128


def test_oracle_api_rejects_bad_input(client):
    response = client.post("/api/oracle", json={"question": "", "shots": 1024})
    assert response.status_code == 400
    assert "error" in response.json


def test_vector_is_disabled_by_default(client):
    response = client.post("/api/vector/speak", json={"text": "Yes"})
    assert response.status_code == 503

