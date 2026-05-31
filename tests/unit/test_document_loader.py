import pytest
from unittest.mock import patch, AsyncMock


@pytest.mark.asyncio
async def test_extract_text_txt(tmp_path):
    file = tmp_path / "test.txt"
    file.write_text("Hello, world!")
    with patch('backend.langchain_workflows.document_processor.load_txt', new_callable=AsyncMock) as mock_load:
        mock_load.return_value = "Hello, world!"
        from backend.langchain_workflows.document_processor import extract_text
        text = await extract_text(str(file))
        assert "Hello, world!" in text
