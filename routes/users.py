from flask import Blueprint, render_template, abort, session
from services import UsersService

users = Blueprint('users', __name__)

@users.route("/<string:username>")
def user_page(username):
    user = UsersService.get_user(username)

    if not user:
        abort(404)

    logged_user_id = -1
    logged_in = "user_id" in session
    if logged_in:
        logged_user_id = session["user_id"]

    reviews = UsersService.get_reviews(user.id, logged_user_id)

    return render_template("user.html", reviews=reviews, user=user)
