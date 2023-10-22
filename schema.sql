DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS restaurants CASCADE;
DROP TABLE IF EXISTS reviews CASCADE;
DROP TABLE IF EXISTS likes CASCADE;
DROP TABLE IF EXISTS review_averages CASCADE;
DROP TABLE IF EXISTS review_likes CASCADE;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT,
    admin BOOLEAN
);
CREATE TABLE restaurants (
    id SERIAL PRIMARY KEY,
    name TEXT,
    description TEXT,
    street_address TEXT,
    postal_code TEXT,
    city TEXT,
    latitude NUMERIC,
    longitude NUMERIC
);
CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    restaurant_id INTEGER REFERENCES restaurants,
    stars INTEGER,
    review TEXT,
    UNIQUE (user_id, restaurant_id)
);
CREATE TABLE likes (
    user_id INTEGER REFERENCES users,
    review_id INTEGER REFERENCES reviews,
    UNIQUE (user_id, review_id)
);
CREATE MATERIALIZED VIEW review_averages AS
    SELECT restaurant_id, avg(stars) AS average FROM reviews GROUP BY restaurant_id;
CREATE MATERIALIZED VIEW review_likes AS
    SELECT r.id AS review_id, count(l.review_id) AS likes
    FROM reviews AS r
    LEFT JOIN likes AS l ON r.id=l.review_id
    GROUP BY r.id;
