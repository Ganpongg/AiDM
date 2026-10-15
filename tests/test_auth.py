import pytest


# ---------------------------------------------------------------------------
# US-001 Register
# ---------------------------------------------------------------------------

class TestRegister:
    def test_register_success(self, client):
        response = client.post("/auth/register", json={
            "email": "user@example.com",
            "password": "secret123",
            "full_name": "Test User",
        })
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "user@example.com"
        assert data["full_name"] == "Test User"
        assert data["is_active"] == 1
        assert "id" in data
        assert "password" not in data
        assert "hashed_password" not in data

    def test_register_without_full_name(self, client):
        response = client.post("/auth/register", json={
            "email": "user@example.com",
            "password": "secret123",
        })
        assert response.status_code == 200
        assert response.json()["full_name"] is None

    def test_register_duplicate_email(self, client):
        payload = {"email": "dup@example.com", "password": "secret123"}
        client.post("/auth/register", json=payload)
        response = client.post("/auth/register", json=payload)
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"].lower()

    def test_register_invalid_email(self, client):
        response = client.post("/auth/register", json={
            "email": "not-an-email",
            "password": "secret123",
        })
        assert response.status_code == 422

    def test_register_missing_password(self, client):
        response = client.post("/auth/register", json={"email": "user@example.com"})
        assert response.status_code == 422

    def test_register_password_not_returned(self, client):
        response = client.post("/auth/register", json={
            "email": "user@example.com",
            "password": "secret123",
        })
        body = response.json()
        assert "password" not in body
        assert "hashed_password" not in body


# ---------------------------------------------------------------------------
# US-002 Login
# ---------------------------------------------------------------------------

class TestLogin:
    def _register(self, client, email="user@example.com", password="secret123"):
        client.post("/auth/register", json={"email": email, "password": password})

    def test_login_success(self, client):
        self._register(client)
        response = client.post("/auth/login", data={
            "username": "user@example.com",
            "password": "secret123",
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self, client):
        self._register(client)
        response = client.post("/auth/login", data={
            "username": "user@example.com",
            "password": "wrongpassword",
        })
        assert response.status_code == 401

    def test_login_unregistered_email(self, client):
        response = client.post("/auth/login", data={
            "username": "nobody@example.com",
            "password": "secret123",
        })
        assert response.status_code == 401

    def test_login_token_is_usable(self, client):
        self._register(client)
        login_res = client.post("/auth/login", data={
            "username": "user@example.com",
            "password": "secret123",
        })
        token = login_res.json()["access_token"]
        me_res = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
        assert me_res.status_code == 200
        assert me_res.json()["email"] == "user@example.com"

    def test_login_missing_fields(self, client):
        response = client.post("/auth/login", data={"username": "user@example.com"})
        assert response.status_code == 422
