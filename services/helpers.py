from sqlalchemy.sql import text
from app import db

def commit():
    db.session.commit()

def execute(sql: str, values: dict | None = None):
    result = db.session.execute(text(sql), values)
    return result
