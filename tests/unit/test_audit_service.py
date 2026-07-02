import pytest
from unittest.mock import AsyncMock, MagicMock


@pytest.fixture
def mock_db():
    db = AsyncMock()
    db.add = MagicMock()
    db.commit = AsyncMock()
    return db


@pytest.mark.asyncio
async def test_log_action(mock_db):
    from backend.services.audit_service import AuditService
    service = AuditService(mock_db)

    await service.log_action(
        user_id="user123",
        action="document_upload",
        resource_type="document",
        resource_id="doc456",
        details="Uploaded test.pdf",
        ip_address="127.0.0.1",
        user_agent="pytest",
    )

    assert mock_db.add.called
    assert mock_db.commit.called
    added_log = mock_db.add.call_args[0][0]
    assert added_log.user_id == "user123"
    assert added_log.action == "document_upload"
    assert added_log.resource_id == "doc456"
    assert added_log.details == "Uploaded test.pdf"


@pytest.mark.asyncio
async def test_log_action_minimal(mock_db):
    from backend.services.audit_service import AuditService
    service = AuditService(mock_db)

    await service.log_action(
        user_id="user123",
        action="ask_question",
        resource_type="document",
    )

    assert mock_db.add.called
    assert mock_db.commit.called
    added_log = mock_db.add.call_args[0][0]
    assert added_log.user_id == "user123"
    assert added_log.action == "ask_question"
    assert added_log.resource_type == "document"
    assert added_log.resource_id is None
    assert added_log.details is None


@pytest.mark.asyncio
async def test_get_user_logs(mock_db):
    from backend.services.audit_service import AuditService
    from datetime import datetime, UTC

    mock_log = MagicMock()
    mock_log.id = "log1"
    mock_log.action = "document_upload"
    mock_log.resource_type = "document"
    mock_log.resource_id = "doc456"
    mock_log.details = "Uploaded file"
    mock_log.timestamp = datetime.now(UTC)
    mock_log.ip_address = "127.0.0.1"
    mock_log.user_agent = "pytest"

    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [mock_log]
    mock_db.execute.return_value = mock_result

    service = AuditService(mock_db)
    logs = await service.get_user_logs("user123", limit=10)

    assert len(logs) == 1
    assert logs[0]["action"] == "document_upload"
    assert logs[0]["resource_id"] == "doc456"


@pytest.mark.asyncio
async def test_get_user_logs_empty(mock_db):
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = []
    mock_db.execute.return_value = mock_result

    from backend.services.audit_service import AuditService
    service = AuditService(mock_db)
    logs = await service.get_user_logs("nonexistent")

    assert logs == []
