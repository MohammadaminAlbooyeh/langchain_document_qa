import re
from typing import Any


class InputSanitizer:
    """Sanitize user inputs to prevent injection attacks"""

    # Common injection patterns
    SQL_INJECTION_PATTERNS = [
        r"(\bDROP\b|\bDELETE\b|\bINSERT\b|\bUPDATE\b|\bSELECT\b|\bEXEC\b)",
        r"(-{2}|/\*|\*/)",  # SQL comments
        r"(;|\||&&)",  # Command separators
    ]

    PROMPT_INJECTION_PATTERNS = [
        r"(ignore|bypass|override|system|instruction|prompt|role)",
    ]

    @staticmethod
    def sanitize_text(text: str, max_length: int = 10000) -> str:
        """Sanitize text input - remove potential injection patterns"""
        if not isinstance(text, str):
            return ""

        # Limit length
        text = text[:max_length]

        # Remove null bytes
        text = text.replace("\x00", "")

        # Remove excessive whitespace
        text = re.sub(r"\s+", " ", text).strip()

        return text

    @staticmethod
    def sanitize_llm_prompt(prompt: str) -> str:
        """Sanitize prompts to prevent LLM prompt injection"""
        prompt = InputSanitizer.sanitize_text(prompt)

        # Remove potential prompt injection keywords (case insensitive)
        for pattern in InputSanitizer.PROMPT_INJECTION_PATTERNS:
            prompt = re.sub(pattern, "", prompt, flags=re.IGNORECASE)

        return prompt.strip()

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize filename to prevent path traversal"""
        # Remove path separators and null bytes
        filename = filename.replace("\\", "").replace("/", "").replace("\x00", "")

        # Remove leading dots (prevent hidden files)
        filename = re.sub(r"^\.+", "", filename)

        # Keep only alphanumeric, dots, underscores, hyphens
        filename = re.sub(r"[^a-zA-Z0-9._-]", "", filename)

        return filename or "file"

    @staticmethod
    def sanitize_email(email: str) -> str:
        """Validate and sanitize email"""
        email = InputSanitizer.sanitize_text(email, max_length=254)

        # Basic email validation
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
            return ""

        return email.lower()

    @staticmethod
    def is_safe_query(query: str) -> bool:
        """Check if a query contains SQL injection patterns"""
        for pattern in InputSanitizer.SQL_INJECTION_PATTERNS:
            if re.search(pattern, query, re.IGNORECASE):
                return False
        return True
