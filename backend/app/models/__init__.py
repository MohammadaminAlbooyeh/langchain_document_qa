from sqlalchemy.orm import declarative_base

Base = declarative_base()

from .house import House  # noqa: E402
from .user import User  # noqa: E402

__all__ = ["Base", "House", "User"]
