from flask import Blueprint, render_template, request, redirect, session, abort, url_for
from services import RestaurantsService, UsersService
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
        restaurant = RestaurantsService.create_restaurant(name, description, street_address, postal_code, city, latitude, longitude)
        return redirect(url_for("restaurants.restaurant_page", restaurant_id=restaurant.id))
    except:
        return "Error creating restaurant"

@restaurants.route("/create")
def create_page():
    return render_template("create_restaurant.html")

@restaurants.route("/<int:restaurant_id>")
def restaurant_page(restaurant_id):
    restaurant = RestaurantsService.get_restaurant(restaurant_id)

    if not restaurant:
        abort(404)

    average_row = RestaurantsService.get_rating(restaurant_id)

    average = 0
    if average_row:
        average = round(average_row.average, 1)

    reviews = RestaurantsService.get_reviews(restaurant_id)

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

    restaurant = RestaurantsService.get_restaurant(restaurant_id)

    if not restaurant:
        abort(404)
    
    user = UsersService.get_user(session["username"])

    if not user:
        abort(403)

    stars = request.form["stars"]
    review = request.form["review"]

    try:
        RestaurantsService.create_review(restaurant_id, user.id, stars, review)
        return redirect(url_for("restaurants.restaurant_page", restaurant_id=restaurant_id))
    except:
        return "Error creating review"
