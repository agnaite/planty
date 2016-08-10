# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, jsonify, flash
from flask_assets import Environment, Bundle

from jinja2 import StrictUndefined

from model import connect_to_db, db, Plant, User, PlantUser
import secret

app = Flask(__name__)
assets = Environment(app)
app.secret_key = secret.APP_KEY

app.jinja_env.undefined = StrictUndefined

# compile sass from sass.scss to all.css
assets.url = app.static_url_path
scss = Bundle('sass.scss', filters='pyscss', output='style.css')
assets.register('scss_all', scss)


@app.route('/')
def index_page():
    """Show index page."""

    return render_template("index.html")


@app.route('/search', methods=['GET'])
def search_for_plant():
    """Displays search results."""

    # gets the user's search term from app.js and queries the db
    search_term = request.args.get('plant-name')
    results = Plant.query.filter(Plant.name.ilike('%' + search_term + '%')).all()

    if len(results) > 0:
        plants_found = {}

        # for each plant in the results, make dictionary using plant's id as key
        # and plant's name as value
        for plant in results:
            plants_found[plant.plant_id] = plant.name

        return jsonify(plants_found)
    else:
        return "No plants found "



@app.route('/plant/<plant_id>')
def show_plant_details(plant_id):
    """Show individual plant's page"""

    plant = Plant.query.get(plant_id)

    return render_template('plant.html',
                            plant_name=plant.name,
                            plant_species=plant.species)


@app.route('/all_plants')
def show_all_plants_by_name():
    """Show all plants by name."""

    all_plants = Plant.query.all()

    return render_template("plants_by_name.html", plants=all_plants)


if __name__ == "__main__":

    connect_to_db(app)
    app.debug = True

    app.run(host="0.0.0.0")
