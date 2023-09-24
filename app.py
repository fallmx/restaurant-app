from flask import Flask
from os import getenv
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")

db = SQLAlchemy(app)

import routes

app.register_blueprint(routes.index, url_prefix="/")
app.register_blueprint(routes.auth, url_prefix="/auth")
app.register_blueprint(routes.restaurants, url_prefix="/restaurants")
