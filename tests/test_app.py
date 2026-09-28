import os
import tempfile
import pytest

@pytest.fixture
def client(monkeypatch):
    fd, path = tempfile.mkstemp()
    os.close(fd)

    import database
    monkeypatch.setattr(database, "DB_PATH", path)

    from database import init_db, seed_db
    init_db()
    seed_db()

    import app
    app.app.config["TESTING"] = True
    app.bot.reload()

    with app.app.test_client() as client:
        yield client

    os.unlink(path)

def test_home(client):
    assert client.get("/").status_code == 200

def test_chat_answer(client):
    response = client.post("/api/chat", json={"message": "What documents are required?"})
    assert response.status_code == 200
    assert "documents" in response.get_json()["answer"].lower()

def test_chat_empty(client):
    response = client.post("/api/chat", json={"message": ""})
    assert response.status_code == 200

def test_admin_requires_login(client):
    assert client.get("/admin").status_code == 302

def test_onboarding_page(client):
    assert client.get("/onboarding").status_code == 200
