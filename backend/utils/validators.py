import re


def validate_file_type(filename: str) -> bool:
    allowed = {".pdf", ".docx", ".txt", ".csv"}
    return any(filename.lower().endswith(ext) for ext in allowed)


def validate_file_size(file_size: int, max_size_mb: int = 100) -> bool:
    return file_size <= max_size_mb * 1024 * 1024


def validate_email(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def validate_language_code(code: str) -> bool:
    valid = {"en", "es", "fr", "de", "it", "pt", "nl", "ja", "ko", "zh", "ar", "ru"}
    return code.lower() in valid
