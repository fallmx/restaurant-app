from sqlalchemy.sql import text
from app import db

def execute(sql: str, values: dict, commit: bool = False):
    result = db.session.execute(text(sql), values)
    if commit: db.session.commit()
    return result
