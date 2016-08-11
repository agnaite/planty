# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, jsonify, flash, url_for
from flask_assets import Environment, Bundle

from jinja2 import StrictUndefined

from model import connect_to_db, db, Plant, User
import secret

app = Flask(__name__)
assets = Environment(app)
app.secret_key = secret.APP_KEY

app.jinja_env.undefined = StrictUndefined

# compile sass from sass.scss to all.css
assets.url = app.static_url_path

scss = Bundle('css/sass.scss', filters='pyscss', output='css/style.css')
assets.register('scss_all', scss)

css = Bundle('css/sweetalert.css')
assets.register('css_all', css)

js = Bundle('js/app.js', 'js/sweetalert.min.js')
assets.register('js_all', js)


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
        return 'None'


@app.route('/plant/<plant_id>')
def show_plant_details(plant_id):
    """Show individual plant's page"""

    plant = Plant.query.get(plant_id)

    return render_template('plant.html',
                           plant_id=plant.plant_id,
                           plant_name=plant.name,
                           plant_species=plant.species,
                           plant_img=plant.image,
                           water=plant.get_water(),
                           sun=plant.get_sun(),
                           humidity=plant.get_humidity(),
                           temp=plant.get_temp())


@app.route('/new_plant')
def add_new_plant():
    """Shows form for adding new plant"""

    WATER = Plant.WATER.keys()
    SUN = Plant.SUN.keys()
    HUMIDITY = Plant.HUMIDITY.keys()
    TEMP = Plant.TEMPERATURE.keys()

    return render_template('new_plant_form.html',
                           WATER=WATER,
                           SUN=SUN,
                           HUMIDITY=HUMIDITY,
                           TEMP=TEMP)


@app.route('/process_new_plant', methods=['POST'])
def process_new_plant():
    """Gets the user input from new plant form and adds to the database"""

    # if plant name not in the db, will create plant, else will not
    name = request.form.get('plant_name').title()
    if Plant.query.filter_by(name=name).all() == []:

        # gets all the user-entered data from the new plant form
        species = request.form.get('plant_species').title()
        image = request.form.get('plant_image')
        water = request.form.get('water')
        sun = request.form.get('sun')
        humidity = request.form.get('humidity')
        temp = request.form.get('temp')

        # creates new plant
        new_plant = Plant(name=name, species=species, image=image, water=water,
                          sun=sun, humidity=humidity, temperature=temp)

        # adds and saves new plant in the database
        db.session.add(new_plant)
        db.session.commit()

        flash(name + " has been added")
        return redirect('/plant/'+str(new_plant.plant_id))
    else:
        flash("Plant already exists", "warning")
        return redirect('/new_plant')


@app.route('/edit_plant', methods=['POST'])
def edit_plant():
    """Edits plant."""

    # gets column being edited, new value, and plant being edited from ajax
    col_to_edit = request.form.get('columnToEdit')
    value = request.form.get('newValue')
    plant_id = int(request.form.get('plantId').plant_id)

    # gets plant being edited and updated the column value for that plant
    Plant.query.filter_by(plant_id=plant_id).update({col_to_edit: value})
    db.session.commit()

    # check to see if col to edit is a plant spec of sun, water, humidity, or temp
    spec = get_plant_specs(Plant.query.get(plant_id), col_to_edit)
    if spec:
        value = spec

    # sends back the the column and new value for html update
    edit = {'col': col_to_edit,
            'val': value}

    return jsonify(edit)


@app.route('/delete_request', methods=['POST'])
def process_delete():
    """Deletes plant from the database"""

    plant_id = int(request.form.get('dataPlant'))
    print '*' * 100
    print plant_id
    plant = Plant.query.get(plant_id)
    print plant
    name = plant.name
    db.session.delete(plant)
    db.session.commit()

    flash(name + ' was deleted')
    return 'done'


@app.route('/all_plants')
def show_all_plants_by_name():
    """Show all plants by name."""

    all_plants = Plant.query.all()

    return render_template("plants_by_name.html", plants=all_plants)

# **************************** HELPER FUNCTIONS *******************************


def get_plant_specs(plant, spec, key='description'):
    """Returns a specific plant attribute for a specific plant"""

    if spec == 'water':
        return plant.get_water(key)
    elif spec == 'sun':
        return plant.get_sun(key)
    elif spec == 'humidity':
        return plant.get_humidity(key)
    elif spec == 'temp':
        return plant.get_temp(key)
    else:
        return None


if __name__ == "__main__":

    connect_to_db(app)
    app.debug = True

    app.run(host="0.0.0.0")
