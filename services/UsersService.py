from services.helpers import execute, commit

class UsersService:
    def get_user(username: str):
        sql = "SELECT id, username, password_hash, admin FROM users WHERE username=:username"
        result = execute(sql, {"username": username})
        return result.fetchone()
    
    def get_reviews(user_id: int, logged_user_id: int = -1):
        sql = """
        SELECT
            rev.id,
            res.id AS restaurant_id,
            res.name AS restaurant_name,
            stars,
            review,
            l.likes,
            EXISTS (SELECT 1 FROM likes WHERE user_id=:logged_user_id AND review_id=rev.id) AS has_liked
        FROM reviews AS rev
        LEFT JOIN restaurants AS res ON rev.restaurant_id=res.id
        LEFT JOIN review_likes AS l ON rev.id=l.review_id
        WHERE rev.user_id=:user_id
        """
        results = execute(sql, {"user_id": user_id, "logged_user_id": logged_user_id})
        return results.fetchall()
        
    def create_user(username: str, password_hash: str, admin: bool):
        sql = "INSERT INTO users (username, password_hash, admin) VALUES (:username, :password_hash, false) RETURNING id"
        result = execute(sql, {"username": username, "password_hash": password_hash, "admin": admin})
        commit()
        return result.fetchone()
