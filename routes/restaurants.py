from flask import Blueprint, render_template, request, redirect, session, abort, url_for
from wtforms import Form, StringField, IntegerField, validators
from services import RestaurantsService
from sqlalchemy.exc import IntegrityError
from geopy.geocoders import Nominatim

geocoder = Nominatim(user_agent="restaurant-app")

restaurants = Blueprint('restaurants', __name__)

class RestaurantForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=35)])
    description = StringField('Description', [validators.Length(max=500)])
    street_address = StringField('Street address', [validators.Length(max=100)])
    postal_code = StringField('Postal code', [validators.Length(max=15)])
    city = StringField('City', [validators.Length(max=100)])

class ReviewForm(Form):
    stars = IntegerField('Stars', [validators.NumberRange(min=1, max=5)])
    review = StringField('Review', [validators.Length(max=1000)])

@restaurants.route("/", methods=["POST"])
def create():
    if not "admin" in session or not "csrf_token" in session:
        abort(403)
    if not session["admin"] or session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    form = RestaurantForm(request.form)
    if not form.validate():
        abort(400)

    name = form.name.data
    description = form.description.data
    street_address = form.street_address.data
    postal_code = form.postal_code.data
    city = form.city.data

    try:
        location = geocoder.geocode({"street": street_address, "postalcode": postal_code, "city": city})
        if not location:
            raise
        latitude = location.latitude
        longitude = location.longitude
    except:
        return render_template("create_restaurant.html", error="Error getting address coordinates")
    
    try:
        restaurant = RestaurantsService.create_restaurant(name, description, street_address, postal_code, city, latitude, longitude)
        return redirect(url_for("restaurants.restaurant_page", restaurant_id=restaurant.id))
    except:
        return render_template("signup.html", error="Error creating restaurant")

@restaurants.route("/create")
def create_page():
    return render_template("create_restaurant.html")

@restaurants.route("/<int:restaurant_id>")
def restaurant_page(restaurant_id):
    restaurant = RestaurantsService.get_restaurant(restaurant_id)

    if not restaurant:
        abort(404)

    logged_user_id = -1
    logged_in = "user_id" in session
    if logged_in:
        logged_user_id = session["user_id"]

    reviews = RestaurantsService.get_reviews(restaurant_id, logged_user_id)

    show_create_review = False
    show_login_prompt = True
    if logged_in:
        already_reviewed = any(r.user_id == session["user_id"] for r in reviews)
        show_create_review = not already_reviewed
        show_login_prompt = False

    return render_template("restaurant.html",
                           restaurant=restaurant,
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

    form = ReviewForm(request.form)

    if not form.validate():
        abort(400)
    
    stars = form.stars.data
    review = form.review.data

    try:
        RestaurantsService.create_review(restaurant_id, session["user_id"], stars, review)
        return redirect(url_for("restaurants.restaurant_page", restaurant_id=restaurant_id))
    except:
        return "Error creating review"

@restaurants.route("/<int:restaurant_id>/reviews/<int:review_id>/like", methods=["POST"])
def like_review(restaurant_id, review_id):
    if not "username" in session:
        return redirect(url_for("auth.login_page", next=url_for("restaurants.restaurant_page", restaurant_id=restaurant_id)))
    
    review = RestaurantsService.get_review(review_id)

    if not review:
        abort(404)

    try:
        RestaurantsService.like_review(session["user_id"], review_id)
        return redirect(request.referrer)
    except IntegrityError:
        return redirect(request.referrer)
    except:
        return "Error liking review"

@restaurants.route("/<int:restaurant_id>/reviews/<int:review_id>/unlike", methods=["POST"])
def unlike_review(restaurant_id, review_id):
    if not "username" in session:
        abort(403)
    
    review = RestaurantsService.get_review(review_id)

    if not review:
        abort(404)

    try:
        RestaurantsService.unlike_review(session["user_id"], review_id)
        return redirect(request.referrer)
    except:
        return "Error unliking review"
