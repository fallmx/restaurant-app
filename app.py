from flask import Flask, render_template, request, session, redirect
from os import getenv
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/login", methods = ['POST'])
def login_submit():
    username = request.form["username"]
    password = request.form["password"]
    sql = "SELECT id, password_hash FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    user = result.fetchone()
    if not user:
        return "Invalid username"
    else:
        password_hash = user.password_hash
        if check_password_hash(password_hash, password):
            session["username"] = username
            return redirect("/")
        else:
            return "Invalid password"

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/signup", methods = ['POST'])
def signup_submit():
    username = request.form["username"]
    password = request.form["password"]
    password_hash = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username, password_hash, admin) VALUES (:username, :password_hash, false)"
        db.session.execute(text(sql), {"username":username, "password_hash":password_hash})
        db.session.commit()
    except:
        return "Error creating user"
    session["username"] = username
    return redirect("/")
