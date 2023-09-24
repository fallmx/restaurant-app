from flask import Blueprint, render_template
from sqlalchemy.sql import text
from app import db

index = Blueprint('index', __name__)

@index.route("/")
def index_page():
    sql = "SELECT id, name FROM restaurants"
    result = db.session.execute(text(sql))
    restaurants = result.fetchall()
    return render_template("index.html", restaurants=restaurants)
