from flask import Blueprint, render_template, request, redirect, session, abort, url_for
from sqlalchemy.sql import text
from app import db
from geopy.geocoders import Nominatim

geocoder = Nominatim(user_agent="restaurant-app")

restaurants = Blueprint('restaurants', __name__)

@restaurants.route("/", methods=["POST"])
def create():
    if not "admin" in session or not "csrf_token" in session:
        abort(403)
    if not session["admin"] or session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    name = request.form["name"]
    description = request.form["description"]
    street_address = request.form["street_address"]
    postal_code = request.form["postal_code"]
    city = request.form["city"]

    try:
        location = geocoder.geocode({"street": street_address, "postalcode": postal_code, "city": city})
        if not location:
            raise
        latitude = location.latitude
        longitude = location.longitude
    except:
        return "Error getting address coordinates"
    
    try:
        sql = "INSERT INTO restaurants (name, description, street_address, postal_code, city, latitude, longitude) VALUES (:name, :description, :street_address, :postal_code, :city, :latitude, :longitude)"
        db.session.execute(text(sql), {"name":name, "description":description, "street_address": street_address, "postal_code": postal_code, "city": city, "latitude": latitude, "longitude": longitude})
        db.session.commit()
        return redirect("/")
    except:
        return "Error creating restaurant"

@restaurants.route("/create")
def create_page():
    return render_template("create_restaurant.html")

@restaurants.route("/<int:restaurant_id>")
def restaurant_page(restaurant_id):
    sql = "SELECT id, name, description FROM restaurants WHERE id=:restaurant_id"
    restaurant_result = db.session.execute(text(sql), {"restaurant_id":restaurant_id})
    restaurant = restaurant_result.fetchone()

    if not restaurant:
        abort(404)

    sql = "SELECT average FROM review_averages WHERE restaurant_id=:restaurant_id"
    average_result = db.session.execute(text(sql), {"restaurant_id":restaurant_id})
    average_row = average_result.fetchone()
    average = 0
    if average_row:
        average = round(average_row.average, 1)

    sql = "SELECT r.id, user_id, u.username, stars, review FROM reviews AS r LEFT JOIN users AS u ON r.user_id=u.id WHERE r.restaurant_id=:restaurant_id"
    review_results = db.session.execute(text(sql), {"restaurant_id":restaurant_id})
    reviews = review_results.fetchall()

    show_create_review = False
    show_login_prompt = True
    if "user_id" in session:
        already_reviewed = any(r.user_id == session["user_id"] for r in reviews)
        show_create_review = not already_reviewed
        show_login_prompt = False

    return render_template("restaurant.html",
                           restaurant=restaurant,
                           average=average,
                           reviews=reviews,
                           show_create_review=show_create_review,
                           show_login_prompt=show_login_prompt)

@restaurants.route("/<int:restaurant_id>/reviews", methods=["POST"])
def create_review(restaurant_id):
    if not "username" in session or not "csrf_token" in session:
        abort(403)
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    sql = "SELECT name, description FROM restaurants WHERE id=:restaurant_id"
    restaurant_result = db.session.execute(text(sql), {"restaurant_id":restaurant_id})
    restaurant = restaurant_result.fetchone()

    if restaurant:
        sql = "SELECT id FROM users WHERE username=:username"
        user_result = db.session.execute(text(sql), {"username":session["username"]})
        user = user_result.fetchone()

        if not user:
            abort(403)

        stars = request.form["stars"]
        review = request.form["review"]
        try:
            sql = "INSERT INTO reviews (user_id, restaurant_id, stars, review) VALUES (:user_id, :restaurant_id, :stars, :review)"
            db.session.execute(text(sql), {"user_id":user.id, "restaurant_id": restaurant_id, "stars":stars, "review": review})
            sql = "REFRESH MATERIALIZED VIEW review_averages"
            db.session.execute(text(sql))
            db.session.commit()
            return redirect(url_for("restaurants.restaurant_page", restaurant_id=restaurant_id))
        except:
            return "Error creating review"
