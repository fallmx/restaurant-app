from flask import Blueprint, render_template, request, session, redirect, abort
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import Form, StringField, validators
from sqlalchemy.exc import IntegrityError
from services import UsersService
from routes.helpers import listErrors
import secrets

auth = Blueprint('auth', __name__)

class AuthForm(Form):
    username = StringField('Username', [validators.Length(min=5, max=25)])
    password = StringField('Password', [validators.Length(min=5, max=64)])

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
    form = AuthForm(request.form)
    if not form.validate():
        return render_template("login.html", next=request.form["next"], error=listErrors(form.errors))
    username = form.username.data
    password = form.password.data
    user = UsersService.get_user(username)
    if not user:
        return render_template("login.html", next=request.form["next"], error="Invalid username")
    else:
        password_hash = user.password_hash
        if check_password_hash(password_hash, password):
            login(username, user.admin, user.id)
            return redirect(request.form["next"])
        else:
            return render_template("login.html", next=request.form["next"], error="Invalid password")

@auth.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@auth.route("/signup")
def signup_page():
    return render_template("signup.html")

@auth.route("/signup", methods = ['POST'])
def signup_submit():
    form = AuthForm(request.form)
    if not form.validate():
        return render_template("signup.html", error=listErrors(form.errors))
    username = form.username.data
    password = form.password.data
    password_hash = generate_password_hash(password)
    try:
        user = UsersService.create_user(username, password_hash, False)
        login(username, False, user.id)
        return redirect("/")
    except IntegrityError:
        return render_template("signup.html", error="Username already exists")
    except:
        return render_template("signup.html", error="Error creating user")
