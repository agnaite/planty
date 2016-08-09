from flask import Flask, render_template
from jinja2 import StrictUndefined
from model import connect_to_db, db, Plant, User, PlantUser
from flask_debugtoolbar import DebugToolbarExtension
import secret

app = Flask(__name__)
app.secret_key = secret.APP_KEY
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index_page():
    """Show index page."""

    return render_template("index.html")


@app.route('/all_plants')
def show_all_plants_by_name():
    """Show all plants by name."""

    all_plants = Plant.query.all()

    return render_template("plants_by_name.html", plants=all_plants)


if __name__ == "__main__":

    connect_to_db(app)
    app.debug = True

    DebugToolbarExtension(app)

    app.run()
