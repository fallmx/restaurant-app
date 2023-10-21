from services.helpers import execute, commit

class UsersService:
    def get_user(username: str):
        sql = "SELECT id, password_hash, admin FROM users WHERE username=:username"
        result = execute(sql, {"username": username})
        return result.fetchone()
        
    def create_user(username: str, password_hash: str, admin: bool):
        sql = "INSERT INTO users (username, password_hash, admin) VALUES (:username, :password_hash, false) RETURNING id"
        result = execute(sql, {"username": username, "password_hash": password_hash, "admin": admin})
        commit()
        return result.fetchone()
