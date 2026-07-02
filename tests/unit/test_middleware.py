import pytest
from unittest.mock import AsyncMock, MagicMock, patch


class TestAuthMiddleware:
    @pytest.mark.asyncio
    async def test_public_paths_skip_auth(self):
        from backend.middleware.auth import AuthMiddleware, PUBLIC_PATHS
        assert "/health" in PUBLIC_PATHS
        assert "/api/v1/auth/login" in PUBLIC_PATHS
        assert "/docs" in PUBLIC_PATHS

    @pytest.mark.asyncio
    async def test_missing_api_key_returns_401(self):
        from backend.middleware.auth import AuthMiddleware

        middleware = AuthMiddleware(AsyncMock())
        mock_request = MagicMock()
        mock_request.url.path = "/api/v1/documents"
        mock_request.headers.get.return_value = None

        call_next = AsyncMock()
        response = await middleware.dispatch(mock_request, call_next)
        assert response.status_code == 401
        assert not call_next.called

    @pytest.mark.asyncio
    async def test_invalid_api_key_returns_401(self):
        from backend.middleware.auth import AuthMiddleware

        with patch('backend.middleware.auth.async_session') as mock_session:
            mock_db = AsyncMock()
            mock_result = MagicMock()
            mock_result.scalar_one_or_none.return_value = None
            mock_db.execute.return_value = mock_result
            mock_session.return_value.__aenter__.return_value = mock_db

            middleware = AuthMiddleware(AsyncMock())
            mock_request = MagicMock()
            mock_request.url.path = "/api/v1/documents"
            mock_request.headers.get.return_value = "lq-invalid"

            call_next = AsyncMock()
            response = await middleware.dispatch(mock_request, call_next)
            assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_valid_api_key_passes(self):
        from backend.middleware.auth import AuthMiddleware

        with patch('backend.middleware.auth.async_session') as mock_session:

            async def mock_iter(*args, **kwargs):
                mock_db = AsyncMock()
                mock_result = MagicMock()

                def scalar_one_or_none():
                    key = MagicMock()
                    key.is_active = True
                    key.expires_at = None
                    key.user_id = "user123"
                    return key
                mock_result.scalar_one_or_none = scalar_one_or_none
                mock_db.execute.return_value = mock_result
                return mock_db

            mock_session.return_value.__aenter__ = mock_iter

            middleware = AuthMiddleware(AsyncMock())
            mock_request = MagicMock()
            mock_request.url.path = "/api/v1/documents"
            mock_request.headers.get.return_value = "lq-valid"
            mock_request.state = MagicMock()

            mock_response = MagicMock()
            call_next = AsyncMock(return_value=mock_response)

            response = await middleware.dispatch(mock_request, call_next)
            assert response == mock_response
            assert call_next.called


class TestRateLimiterMiddleware:
    @pytest.mark.asyncio
    async def test_allows_requests_under_limit(self):
        from backend.middleware.rate_limiter import RateLimiterMiddleware

        middleware = RateLimiterMiddleware(AsyncMock(), max_requests=100, window_seconds=60)
        mock_request = MagicMock()
        mock_request.client.host = "127.0.0.1"

        mock_response = MagicMock()
        call_next = AsyncMock(return_value=mock_response)

        response = await middleware.dispatch(mock_request, call_next)
        assert response == mock_response

    @pytest.mark.asyncio
    async def test_blocks_requests_over_limit(self):
        from backend.middleware.rate_limiter import RateLimiterMiddleware

        middleware = RateLimiterMiddleware(AsyncMock(), max_requests=2, window_seconds=60)
        mock_request = MagicMock()
        mock_request.client.host = "127.0.0.1"

        mock_response = MagicMock()
        call_next = AsyncMock(return_value=mock_response)

        await middleware.dispatch(mock_request, call_next)
        await middleware.dispatch(mock_request, call_next)
        response = await middleware.dispatch(mock_request, call_next)
        assert response.status_code == 429


class TestRequestIDMiddleware:
    @pytest.mark.asyncio
    async def test_adds_request_id_to_response(self):
        from backend.middleware.request_id import RequestIDMiddleware

        middleware = RequestIDMiddleware(AsyncMock())
        mock_request = MagicMock()
        mock_request.headers.get.return_value = None

        mock_response = MagicMock()
        mock_response.headers = {}
        call_next = AsyncMock(return_value=mock_response)

        response = await middleware.dispatch(mock_request, call_next)
        assert "X-Request-ID" in response.headers


class TestTimingMiddleware:
    @pytest.mark.asyncio
    async def test_adds_response_time_header(self):
        from backend.middleware.timing import TimingMiddleware

        middleware = TimingMiddleware(AsyncMock())
        mock_request = MagicMock()
        mock_request.method = "GET"
        mock_request.url.path = "/test"

        mock_response = MagicMock()
        mock_response.headers = {}
        call_next = AsyncMock(return_value=mock_response)

        with patch('backend.middleware.timing.logger'):
            response = await middleware.dispatch(mock_request, call_next)
            assert "X-Response-Time" in response.headers


class TestErrorHandler:
    def test_custom_exception_handler_registered(self):
        from backend.main import app
        handlers = [r for r in app.exception_handlers.values()]
        assert len(handlers) > 0
