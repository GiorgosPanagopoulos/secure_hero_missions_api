import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.db import get_session
from app.main import app
from app.models import User
from app.security import hash_password


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


def _register_and_login(client: TestClient, username: str, password: str) -> str:
    client.post("/auth/register", json={"username": username, "password": password})
    response = client.post(
        "/auth/login", data={"username": username, "password": password}
    )
    return response.json()["access_token"]


def test_register_user(client: TestClient):
    response = client.post(
        "/auth/register", json={"username": "hero_user", "password": "secret123"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "hero_user"
    assert "password" not in data


def test_login_returns_token(client: TestClient):
    client.post("/auth/register", json={"username": "tokenuser", "password": "pass123"})
    response = client.post(
        "/auth/login", data={"username": "tokenuser", "password": "pass123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_create_hero_requires_authentication(client: TestClient):
    response = client.post(
        "/heroes/", json={"name": "Spider", "power": "Web", "level": 5}
    )
    assert response.status_code == 401


def test_create_hero_with_token(client: TestClient):
    token = _register_and_login(client, "heromaker", "pass123")
    response = client.post(
        "/heroes/",
        json={"name": "Ironman", "power": "Genius", "level": 10},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Ironman"


def test_create_mission_for_missing_hero_returns_404(client: TestClient):
    token = _register_and_login(client, "missionuser", "pass123")
    response = client.post(
        "/missions/",
        json={"title": "Find the villain", "difficulty": 5, "hero_id": 999},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404


def test_normal_user_cannot_delete_hero(client: TestClient):
    token = _register_and_login(client, "normaluser", "pass123")

    hero_resp = client.post(
        "/heroes/",
        json={"name": "Batman", "power": "Money", "level": 7},
        headers={"Authorization": f"Bearer {token}"},
    )
    hero_id = hero_resp.json()["id"]

    response = client.delete(
        f"/heroes/{hero_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 403


def test_admin_can_delete_mission(client: TestClient, session: Session):
    admin = User(
        username="admin_hero",
        hashed_password=hash_password("adminpass"),
        is_admin=True,
    )
    session.add(admin)
    session.commit()

    login_resp = client.post(
        "/auth/login", data={"username": "admin_hero", "password": "adminpass"}
    )
    token = login_resp.json()["access_token"]
    auth_headers = {"Authorization": f"Bearer {token}"}

    hero_resp = client.post(
        "/heroes/",
        json={"name": "Superman", "power": "Flight", "level": 10},
        headers=auth_headers,
    )
    hero_id = hero_resp.json()["id"]

    mission_resp = client.post(
        "/missions/",
        json={"title": "Save the city now", "difficulty": 8, "hero_id": hero_id},
        headers=auth_headers,
    )
    mission_id = mission_resp.json()["id"]

    response = client.delete(f"/missions/{mission_id}", headers=auth_headers)
    assert response.status_code == 204
