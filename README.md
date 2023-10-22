# restaurant-app

A website to rate restaurants. You can

- see restaurants on a map,

- rate restaurants,

- filter/order restaurants by text and ratings,

- view ratings made by a user,

- like ratings,

- add new restaurants as an admin.

## Testing locally
Clone the repository:
```bash
git clone https://github.com/fallmx/restaurant-app.git
```
Activate the Python virtual environment:
```bash
python3 -m venv venv
source ./venv/bin/activate
```
Install the dependencies:
```bash
pip install -r ./requirements.txt
```
Create a `.env` file in the root directory with the following content:
```bash
DATABASE_URL=<Insert your PostgreSQL database url>
SECRET_KEY=<Insert a strong secret key>
```
Seed the database with some mock data (Warning: it will drop some tables in the connected database, see `schema.sql`). It will also create an admin user with the username `admin` and password `admin`:
```bash
python3 ./seed.py
```
Start the application:
```bash
flask run
```
The website should now be running on `http://localhost:5000`. You can create a new user or log in as an admin user with the credentials mentioned above.
