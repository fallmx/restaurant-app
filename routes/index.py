from flask import Blueprint, render_template, request
from services import RestaurantsService

index = Blueprint('index', __name__)

@index.route("/")
def index_page():
    search = request.args.get("search", "")
    sort = request.args.get("sort", "rating_desc")
    restaurants = RestaurantsService.get_restaurants(search, sort)
    return render_template("index.html", restaurants=restaurants)
