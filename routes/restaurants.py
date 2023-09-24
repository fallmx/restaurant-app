from flask import Blueprint, render_template, request, redirect, session, abort
from sqlalchemy.sql import text
from app import db

restaurants = Blueprint('restaurants', __name__)

@restaurants.route("/", methods=["POST"])
def create():
    if not "admin" in session or not "csrf_token" in session:
        abort(403)
    if not session["admin"] or session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    name = request.form["name"]
    description = request.form["description"]
    try:
        sql = "INSERT INTO restaurants (name, description) VALUES (:name, :description)"
        db.session.execute(text(sql), {"name":name, "description":description})
        db.session.commit()
        return redirect("/")
    except:
        return "Error creating restaurant"

@restaurants.route("/create")
def create_page():
    return render_template("create_restaurant.html")

@restaurants.route("/<int:restaurant_id>")
def restaurant_page(restaurant_id):
    sql = "SELECT name, description FROM restaurants WHERE id=:restaurant_id"
    result = db.session.execute(text(sql), {"restaurant_id":restaurant_id})
    restaurant = result.fetchone()
    return render_template("restaurant.html", restaurant=restaurant)
