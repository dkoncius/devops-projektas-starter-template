import importlib
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.delenv("DB_HOST", raising=False)
    monkeypatch.setenv("SQLITE_PATH", str(tmp_path / "test.db"))
    import app as app_module

    importlib.reload(app_module)
    return app_module.app.test_client()


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json() == {"status": "ok"}


def test_items_list_and_add(client):
    assert len(client.get("/items").get_json()) == 3
    r = client.post("/items", json={"name": "Testas"})
    assert r.status_code == 201
    assert client.get("/items").get_json()[-1]["name"] == "Testas"


def test_add_empty_name(client):
    assert client.post("/items", json={"name": " "}).status_code == 400
