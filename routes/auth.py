from flask import Blueprint, render_template, request, session, redirect
from werkzeug.security import check_password_hash, generate_password_hash
from services import UsersService
import secrets

auth = Blueprint('auth', __name__)

def login(username: str, admin: bool, user_id: int):
    session["username"] = username
    session["admin"] = admin
    session["user_id"] = user_id
    session["csrf_token"] = secrets.token_hex(16)

@auth.route("/login")
def login_page():
    next = request.args.get("next", "/")
    return render_template("login.html", next=next)

@auth.route("/login", methods = ['POST'])
def login_submit():
    username = request.form["username"]
    password = request.form["password"]
    user = UsersService.get_user(username)
    if not user:
        return "Invalid username"
    else:
        password_hash = user.password_hash
        if check_password_hash(password_hash, password):
            login(username, user.admin, user.id)
            return redirect(request.form["next"])
        else:
            return "Invalid password"

@auth.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@auth.route("/signup")
def signup_page():
    return render_template("signup.html")

@auth.route("/signup", methods = ['POST'])
def signup_submit():
    username = request.form["username"]
    password = request.form["password"]
    password_hash = generate_password_hash(password)
    try:
        user = UsersService.create_user(username, password_hash, False)
        login(username, False, user.id)
        return redirect("/")
    except:
        return "Error creating user"
