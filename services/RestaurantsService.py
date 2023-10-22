from services.helpers import execute, commit

class RestaurantsService:
    def get_restaurants(search: str, sort: str = None):
        sql = """
        SELECT id, name, latitude, longitude, coalesce(average, 0) AS average
        FROM restaurants AS res
        LEFT JOIN review_averages AS avg ON res.id=avg.restaurant_id
        WHERE position(lower(:search) in lower(name))>0
        """
        if sort == "rating_desc":
            sql += " ORDER BY average DESC"
        if sort == "rating_asc":
            sql += " ORDER BY average ASC"
        result = execute(sql, {"search": search})
        restaurants = result.fetchall()
        return [row._asdict() for row in restaurants]
    
    def get_restaurant(restaurant_id: int):
        sql = """
        SELECT id, name, description, coalesce(average, 0) AS average
        FROM restaurants AS res
        LEFT JOIN review_averages AS avg ON res.id=avg.restaurant_id
        WHERE id=:restaurant_id
        """
        result = execute(sql, {"restaurant_id":restaurant_id})
        return result.fetchone()
    
    def get_reviews(restaurant_id: int, logged_user_id: int = -1):
        sql = """
        SELECT
            r.id,
            r.user_id,
            u.username,
            stars,
            review,
            l.likes,
            EXISTS (SELECT 1 FROM likes WHERE user_id=:logged_user_id AND review_id=r.id) AS has_liked
        FROM reviews AS r
        LEFT JOIN users AS u ON r.user_id=u.id
        LEFT JOIN review_likes AS l ON r.id=l.review_id
        WHERE r.restaurant_id=:restaurant_id;
        """
        results = execute(sql, {"restaurant_id":restaurant_id, "logged_user_id": logged_user_id})
        return results.fetchall()
    
    def get_review(review_id: int):
        sql = "SELECT id FROM reviews WHERE id=:review_id"
        result = execute(sql, {"review_id":review_id})
        return result.fetchone()
    
    def create_restaurant(name: str, description: str, street_address: str, postal_code: str, city: str, latitude: str, longitude: str):
        sql = "INSERT INTO restaurants (name, description, street_address, postal_code, city, latitude, longitude) VALUES (:name, :description, :street_address, :postal_code, :city, :latitude, :longitude) RETURNING id"
        result = execute(sql, {"name":name, "description":description, "street_address": street_address, "postal_code": postal_code, "city": city, "latitude": latitude, "longitude": longitude})
        commit()
        return result.fetchone()
    
    def create_review(restaurant_id: int, user_id: int, stars: int, review: str):
        sql = "INSERT INTO reviews (user_id, restaurant_id, stars, review) VALUES (:user_id, :restaurant_id, :stars, :review)"
        execute(sql, {"user_id":user_id, "restaurant_id": restaurant_id, "stars":stars, "review": review})
        execute("REFRESH MATERIALIZED VIEW review_averages")
        execute("REFRESH MATERIALIZED VIEW review_likes")
        commit()

    def like_review(user_id: int, review_id: int):
        sql = "INSERT INTO likes (user_id, review_id) VALUES (:user_id, :review_id)"
        execute(sql, {"user_id": user_id, "review_id": review_id})
        execute("REFRESH MATERIALIZED VIEW review_likes")
        commit()

    def unlike_review(user_id: int, review_id: int):
        sql = "DELETE FROM likes WHERE user_id=:user_id AND review_id=:review_id"
        execute(sql, {"user_id": user_id, "review_id": review_id})
        execute("REFRESH MATERIALIZED VIEW review_likes")
        commit()
