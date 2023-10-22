from flask import Blueprint, render_template, abort
from services import UsersService

users = Blueprint('users', __name__)

@users.route("/<string:username>")
def user_page(username):
    user = UsersService.get_user(username)

    if not user:
        abort(404)

    reviews = UsersService.get_reviews(user.id)

    return render_template("user.html", reviews=reviews, user=user)
