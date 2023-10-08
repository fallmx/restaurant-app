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

    def create_restaurant(name, description, street_address, postal_code, city, latitude, longitude):
        sql = "INSERT INTO restaurants (name, description, street_address, postal_code, city, latitude, longitude) VALUES (:name, :description, :street_address, :postal_code, :city, :latitude, :longitude)"
        conn.execute(text(sql), {"name":name, "description":description, "street_address": street_address, "postal_code": postal_code, "city": city, "latitude": latitude, "longitude": longitude})

    create_restaurant("Pizzeria", "An italian pizzeria.", "Hämeentie 111", "00560", "Helsinki", "60.203316055160606", "24.969218606116698")
    create_restaurant("Ramen-shop", "Japanese ramen.", "Helsinginkatu 20", "00530", "Helsinki", "60.18677926782581", "24.951847626706268")
    create_restaurant("Taco-foodtruck", "A foodtruck serving tacos.", "Hietalahdentori", "00180", "Helsinki", "60.16277062521797", "24.93009142165094")

    conn.commit()
    conn.close()
