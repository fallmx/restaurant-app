from services.helpers import execute, commit

class UsersService:
    def get_user(username: str):
        sql = "SELECT id, username, password_hash, admin FROM users WHERE username=:username"
        result = execute(sql, {"username": username})
        return result.fetchone()
    
    def get_reviews(user_id: int):
        sql = "SELECT rev.id AS id, stars, review, res.id AS restaurant_id, res.name AS restaurant_name FROM reviews AS rev LEFT JOIN restaurants AS res ON rev.restaurant_id=res.id WHERE rev.user_id=:user_id"
        results = execute(sql, {"user_id":user_id})
        return results.fetchall()
        
    def create_user(username: str, password_hash: str, admin: bool):
        sql = "INSERT INTO users (username, password_hash, admin) VALUES (:username, :password_hash, false) RETURNING id"
        result = execute(sql, {"username": username, "password_hash": password_hash, "admin": admin})
        commit()
        return result.fetchone()
