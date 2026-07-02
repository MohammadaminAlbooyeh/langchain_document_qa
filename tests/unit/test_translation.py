import pytest
from unittest.mock import patch, MagicMock, AsyncMock


@pytest.mark.asyncio
async def test_detect_language():
    from backend.langchain_workflows.translation_chain import detect_language

    with patch('backend.langchain_workflows.translation_chain._llm') as mock_llm:
        mock_response = MagicMock()
        mock_response.content = "French"
        mock_llm.ainvoke.return_value = mock_response

        result = await detect_language("Bonjour le monde")
        assert result == "French"


@pytest.mark.asyncio
async def test_translate():
    from backend.langchain_workflows.translation_chain import translate

    with patch('backend.langchain_workflows.translation_chain._llm') as mock_llm:
        mock_response = MagicMock()
        mock_response.content = "Hello world"
        mock_llm.ainvoke.return_value = mock_response

        result = await translate("Bonjour le monde", "english", "French")
        assert result == "Hello world"


@pytest.mark.asyncio
async def test_translate_document():
    from backend.langchain_workflows.translation_chain import translate_document

    with patch('backend.langchain_workflows.translation_chain.detect_language', new_callable=AsyncMock) as mock_detect:
        mock_detect.return_value = "French"
        with patch('backend.langchain_workflows.translation_chain.translate', new_callable=AsyncMock) as mock_translate:
            mock_translate.return_value = "Hello world"

            result = await translate_document("Bonjour le monde", "english")
            assert result["source_language"] == "French"
            assert result["target_language"] == "english"
            assert result["translated_text"] == "Hello world"


@pytest.mark.asyncio
async def test_translate_service():
    from backend.services.translation_service import TranslationService

    with patch('backend.services.translation_service.translate_document', new_callable=AsyncMock) as mock_translate_doc:
        mock_translate_doc.return_value = {
            "source_language": "French",
            "target_language": "english",
            "translated_text": "Hello world",
        }

        service = TranslationService()
        result = await service.translate("Bonjour le monde", "english")
        assert result["source_language"] == "French"
        assert result["translated_text"] == "Hello world"


def test_translation_prompt_template():
    from backend.langchain_workflows.prompt_templates import translation_prompt
    formatted = translation_prompt.format(text="Hello", target_language="French")
    assert "Hello" in formatted
    assert "French" in formatted
