import uuid
import hashlib
from datetime import datetime


def generate_id() -> str:
    return str(uuid.uuid4())


def generate_hash(content: str) -> str:
    return hashlib.sha256(content.encode()).hexdigest()


def truncate_text(text: str, max_length: int = 200) -> str:
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def format_timestamp(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def safe_filename(filename: str) -> str:
    import re
    return re.sub(r"[^\w\-_.]", "_", filename)
