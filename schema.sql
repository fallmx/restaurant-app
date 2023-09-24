DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS restaurants;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT,
    admin BOOLEAN
);
CREATE TABLE restaurants (
    id SERIAL PRIMARY KEY,
    name TEXT,
    description TEXT
);
