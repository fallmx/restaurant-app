from dotenv import load_dotenv
from os import environ
from sqlalchemy import create_engine, text
from werkzeug.security import generate_password_hash

load_dotenv()

engine = create_engine(environ["DATABASE_URL"])

with engine.begin() as conn:
    with open("schema.sql") as f:
        conn.execute(text(f.read()))
    password_hash = generate_password_hash("admin")
    sql = "INSERT INTO users (username, password_hash, admin) VALUES ('admin', :password_hash, true)"
    conn.execute(text(sql), {"password_hash":password_hash})

    def create_restaurant(name, description):
        sql = "INSERT INTO restaurants (name, description) VALUES (:name, :description)"
        conn.execute(text(sql), {"name":name, "description":description})

    create_restaurant("Pizzeria", "An italian pizzeria.")
    create_restaurant("Ramen-shop", "Japanese ramen.")
    create_restaurant("Taco-foodtruck", "A foodtruck serving tacos.")

    conn.commit()
    conn.close()
