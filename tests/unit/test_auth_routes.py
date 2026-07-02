import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from httpx import AsyncClient, ASGITransport


@pytest.fixture
def app():
    from backend.main import app
    return app


@pytest.fixture
async def client(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_login_generates_api_key(client):
    with patch('backend.api.auth_routes.get_db_session') as mock_get_db:
        mock_db = AsyncMock()
        mock_db.add = MagicMock()
        mock_db.commit = AsyncMock()
        mock_get_db.return_value.__aenter__.return_value = mock_db

        mock_get_db.return_value.__aiter__.return_value = iter([mock_db])

        with patch('backend.api.auth_routes.generate_api_key', return_value="lq-testkey123"):
            with patch('backend.middleware.auth.AuthMiddleware.dispatch', side_effect=lambda req, call_next: call_next(req)):
                response = await client.post(
                    "/api/v1/auth/login",
                    json={"email": "test@example.com", "password": "password123"},
                )

                assert response.status_code == 200
                data = response.json()
                assert "token" in data
                assert "user_id" in data
                assert data["token"] == "lq-testkey123"


@pytest.mark.asyncio
async def test_login_fails_with_invalid_email(client):
    with patch('backend.middleware.auth.AuthMiddleware.dispatch', side_effect=lambda req, call_next: call_next(req)):
        response = await client.post(
            "/api/v1/auth/login",
            json={"email": "not-an-email", "password": "password123"},
        )
        assert response.status_code == 400


@pytest.mark.asyncio
async def test_verify_valid_key(client):
    with patch('backend.api.auth_routes.get_db_session') as mock_get_db:
        mock_db = AsyncMock()
        mock_result = MagicMock()
        mock_key = MagicMock()
        mock_key.is_active = True
        mock_key.user_id = "user123"
        mock_key.expires_at = None
        mock_result.scalar_one_or_none.return_value = mock_key
        mock_db.execute.return_value = mock_result
        mock_db.commit = AsyncMock()
        mock_get_db.return_value.__aiter__.return_value = iter([mock_db])

        with patch('backend.middleware.auth.AuthMiddleware.dispatch', side_effect=lambda req, call_next: call_next(req)):
            response = await client.post(
                "/api/v1/auth/verify",
                headers={"X-API-Key": "lq-validkey"},
            )
            assert response.status_code == 200
            data = response.json()
            assert data["valid"] is True
            assert data["user_id"] == "user123"


@pytest.mark.asyncio
async def test_verify_expired_key(client):
    from datetime import datetime, UTC, timedelta

    with patch('backend.api.auth_routes.get_db_session') as mock_get_db:
        mock_db = AsyncMock()
        mock_result = MagicMock()
        mock_key = MagicMock()
        mock_key.is_active = True
        mock_key.user_id = "user123"
        mock_key.expires_at = datetime.now(UTC) - timedelta(days=1)
        mock_result.scalar_one_or_none.return_value = mock_key
        mock_db.execute.return_value = mock_result
        mock_get_db.return_value.__aiter__.return_value = iter([mock_db])

        with patch('backend.middleware.auth.AuthMiddleware.dispatch', side_effect=lambda req, call_next: call_next(req)):
            response = await client.post(
                "/api/v1/auth/verify",
                headers={"X-API-Key": "lq-expiredkey"},
            )
            assert response.status_code == 401


@pytest.mark.asyncio
async def test_verify_invalid_key(client):
    with patch('backend.api.auth_routes.get_db_session') as mock_get_db:
        mock_db = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db.execute.return_value = mock_result
        mock_get_db.return_value.__aiter__.return_value = iter([mock_db])

        with patch('backend.middleware.auth.AuthMiddleware.dispatch', side_effect=lambda req, call_next: call_next(req)):
            response = await client.post(
                "/api/v1/auth/verify",
                headers={"X-API-Key": "lq-invalidkey"},
            )
            assert response.status_code == 401


@pytest.mark.asyncio
async def test_revoke_key(client):
    with patch('backend.api.auth_routes.get_db_session') as mock_get_db:
        mock_db = AsyncMock()
        mock_result = MagicMock()
        mock_key = MagicMock()
        mock_key.is_active = True
        mock_key.key = "lq-revokable"
        mock_result.scalar_one_or_none.return_value = mock_key
        mock_db.execute.return_value = mock_result
        mock_db.commit = AsyncMock()
        mock_get_db.return_value.__aiter__.return_value = iter([mock_db])

        with patch('backend.middleware.auth.AuthMiddleware.dispatch', side_effect=lambda req, call_next: call_next(req)):
            response = await client.post(
                "/api/v1/auth/revoke",
                headers={"X-API-Key": "lq-revokable"},
            )
            assert response.status_code == 200
            assert mock_key.is_active is False


def test_generate_api_key_prefix():
    from backend.api.auth_routes import generate_api_key
    key = generate_api_key()
    assert key.startswith("lq-")
    assert len(key) > 10
