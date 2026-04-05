from .database import init_db as _init_db


def create_all():
    _init_db()
