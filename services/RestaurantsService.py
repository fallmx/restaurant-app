from services.helpers import execute, commit

class RestaurantsService:
    def get_restaurants():
        sql = "SELECT id, name, latitude, longitude FROM restaurants"
        result = execute(sql)
        restaurants = result.fetchall()
        return [row._asdict() for row in restaurants]
    
    def get_restaurant(restaurant_id: int):
        sql = "SELECT id, name, description FROM restaurants WHERE id=:restaurant_id"
        result = execute(sql, {"restaurant_id":restaurant_id})
        return result.fetchone()
    
    def get_rating(restaurant_id: int):
        sql = "SELECT average FROM review_averages WHERE restaurant_id=:restaurant_id"
        result = execute(sql, {"restaurant_id":restaurant_id})
        return result.fetchone()
    
    def get_reviews(restaurant_id: int):
        sql = "SELECT r.id, user_id, u.username, stars, review FROM reviews AS r LEFT JOIN users AS u ON r.user_id=u.id WHERE r.restaurant_id=:restaurant_id"
        results = execute(sql, {"restaurant_id":restaurant_id})
        return results.fetchall()
    
    def create_restaurant(name: str, description: str, street_address: str, postal_code: str, city: str, latitude: str, longitude: str):
        sql = "INSERT INTO restaurants (name, description, street_address, postal_code, city, latitude, longitude) VALUES (:name, :description, :street_address, :postal_code, :city, :latitude, :longitude) RETURNING id"
        result = execute(sql, {"name":name, "description":description, "street_address": street_address, "postal_code": postal_code, "city": city, "latitude": latitude, "longitude": longitude})
        commit()
        return result.fetchone()
    
    def create_review(restaurant_id: int, user_id: int, stars: int, review: str):
        sql = "INSERT INTO reviews (user_id, restaurant_id, stars, review) VALUES (:user_id, :restaurant_id, :stars, :review)"
        execute(sql, {"user_id":user_id, "restaurant_id": restaurant_id, "stars":stars, "review": review})
        execute("REFRESH MATERIALIZED VIEW review_averages")
        commit()
