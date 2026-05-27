import pytest
from backend.langchain_workflows.document_processor import extract_text


@pytest.mark.asyncio
async def test_extract_text_txt(tmp_path):
    file = tmp_path / "test.txt"
    file.write_text("Hello, world!")
    text = await extract_text(str(file))
    assert "Hello, world!" in text
