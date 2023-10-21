from flask import Blueprint, render_template
from services import RestaurantsService

index = Blueprint('index', __name__)

@index.route("/")
def index_page():
    restaurants = RestaurantsService.get_restaurants()
    return render_template("index.html", restaurants=restaurants)
