# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, jsonify, flash, session
from flask_assets import Environment
import simplejson
import random
import secret
import flickr_api
from flickr_api.api import flickr
from jinja2 import StrictUndefined
from datetime import datetime

from model import connect_to_db, db, Plant, User, PlantUser

app = Flask(__name__)

assets = Environment(app)

app.jinja_env.undefined = StrictUndefined
assets.url = app.static_url_path
app.config['ASSETS_DEBUG'] = True
app.secret_key = secret.APP_KEY
flickr_api_key = secret.FLICKR_API_KEY
flickr_api_secret = secret.FLICKR_API_SECRET

flickr_api.set_keys(api_key=flickr_api_key,
                    api_secret=flickr_api_secret)

# ************************* ROUTES *********************************

# Basic Routes *********************************


@app.route('/')
def index_page():
    """Show index page."""
    return render_template("base.html")


# sends static html files to angular
@app.route('/html_for_angular/<filename>')
def html_for_angular(filename):
    return render_template('angular/{}'.format(filename))


@app.route('/search/<search_term>')
def search_for_plant(search_term):
    """Retrieves search results from database."""

    # gets the user's search term from app.js and queries the db
    results = Plant.query.filter(Plant.name.ilike('%' + search_term + '%')).all()

    if results:
        plants_found = {}

        # for each plant in the results, make dictionary using plant's id as key
        # and plant's other data as value
        for plant in results:
            plants_found[plant.plant_id] = {'id': plant.plant_id,
                                            'name': plant.name}

        return jsonify(plants_found)
    else:
        return 'None'


# User Routes *********************************

@app.route('/user/<user_id>')
def get_user_info(user_id):
    """Retrieves user data based on the user ID."""

    user = User.query.get(user_id)
    user = user.__dict__

    if '_sa_instance_state' in user:
        del user['_sa_instance_state']

    user_plants = get_user_plants(user_id)

    user['plants'] = user_plants

    for plant in user['plants']:
        user['plants'][plant]['reminder_status'] = str(get_reminder_status(user['user_id'], user['plants'][plant]['plant_id']))

    return jsonify(user)


@app.route('/is_username/<username>')
def check_if_username_is_taken(username):
    """Checks if a username has already been taken.

       Returns true if username exists, and false otherwise.

    """
    username = username.lower()
    user = User.query.filter_by(username=username).first()

    if user:
        return "True"
    else:
        return "False"


@app.route('/is_email/<email>')
def check_if_email_is_taken(email):
    """Checks if a email is already in use.

       Returns true if email exists, and false otherwise.

    """
    email = email.lower()
    user = User.query.filter_by(email=email).first()

    if user:
        return "True"
    else:
        return "False"


@app.route('/process_login', methods=['POST'])
def process_login():
    """Processes user input and either logs user in if input is in database"""

    # gets the user input from the username field and looks it up in the database
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()

    # if username entered exists in db, gets the password entered and compares
    # it to the one in the database
    if user:
        password = hash(request.form.get('password'))
        # if password is correct, adds user to the current session and redirects to home page
        if user.password == str(password):
            session['logged_in'] = user.user_id
            print 'logged in'
            return jsonify(session)
        # if password is incorrect, redirects to login page
        else:
            return 'error'
    # if username is not in the database, redirects to the registration form
    else:
        return 'error'


@app.route('/process_logout')
def process_logout():
    """Processes user logout"""

    del session['logged_in']

    return 'logged out'


@app.route('/process_registration', methods=['POST'])
def process_registration():
    """Processes user registration form"""

    # creates a new user instance
    new_user = User(username=request.form.get('username'),
                    first_name=request.form.get('fname'),
                    last_name=request.form.get('lname'),
                    password=hash(request.form.get('password')),
                    email=request.form.get('email'),
                    image=request.form.get('image'),
                    phone=request.form.get('phone'),
                    confirmed_at=datetime.now())

    # adds the new user instance to the database and saves
    db.session.add(new_user)
    db.session.commit()

    # logs new user in
    session['logged_in'] = new_user.user_id

    return str(new_user.user_id)


# PlantUser Routes *********************************

@app.route('/add_user_plant', methods=['POST'])
def add_plant_to_user():
    """Add a plant to a User's account."""

    user_id = int(request.form.get('userId'))
    plant_id = int(request.form.get('plantId'))

    new_plantuser = PlantUser(user_id=user_id, plant_id=plant_id)

    db.session.add(new_plantuser)
    db.session.commit()

    return 'ok'


@app.route('/remove_user_plant', methods=['POST'])
def remove_plant_from_user():
    """Delete a plant from a User's account."""

    user_id = int(request.form.get('userId'))
    plant_id = int(request.form.get('plantId'))

    plantuser = PlantUser.query.filter(PlantUser.user_id == user_id, PlantUser.plant_id == plant_id).first()

    db.session.delete(plantuser)
    db.session.commit()

    return 'ok'


@app.route('/is_plant_user', methods=['POST'])
def does_user_own_plant():
    """Checks if a user has already added that specific plant."""
    try:
        user = User.query.get(int(request.form.get('userId')))
    except:
        return 'not logged in'

    plant = Plant.query.get(int(request.form.get('plantId')))

    print plant
    print user.plants

    if plant in user.plants:
        return 'true'
    else:
        return 'false'


@app.route('/process_new_reminder', methods=['POST'])
def add_reminder():
    """Adds a watering reminder for a particular PlantUser"""

    plant_id = int(request.form.getlist('plant_id')[0].encode('utf-8'))
    user_id = int(request.form.getlist('user_id')[0].encode('utf-8'))
    days = request.form.getlist('days')[0].encode('utf-8')

    plant_user = PlantUser.query.filter(PlantUser.user_id == user_id, PlantUser.plant_id == plant_id).first()
    plant_user.watering_schedule = days

    db.session.commit()

    return 'ok'


@app.route('/delete_reminder', methods=['POST'])
def delete_reminder():
    """Deletes a watering reminder for a particular PlantUser"""

    plant_id = int(request.form.getlist('plant_id')[0].encode('utf-8'))
    user_id = int(request.form.getlist('user_id')[0].encode('utf-8'))

    plant_user = PlantUser.query.filter(PlantUser.user_id == user_id, PlantUser.plant_id == plant_id).first()
    plant_user.watering_schedule = ''

    db.session.commit()

    return 'ok'


# Plant Routes *********************************


@app.route('/plant/<plant_id>')
def show_plant_details(plant_id):
    """Show individual plant's page"""

    found_plant = Plant.query.get(plant_id)

    if not found_plant.image:
        found_plant.image = "/static/img/placeholder-image.png"

        db.session.commit()

    found_plant = found_plant.__dict__

    if '_sa_instance_state' in found_plant:
        del found_plant['_sa_instance_state']

    return jsonify(found_plant)


@app.route('/is_plant/<plant_name>')
def get_all_plant_names(plant_name):
    """Checks if a plant by a specific name is already in the database.

       Returns true if plant by that name exists, and false otherwise.

    """
    plant_name = plant_name.title()
    plant = Plant.query.filter_by(name=plant_name).first()

    if plant:
        return "True"
    else:
        return "False"


@app.route('/get_flickr_img/<plant_name>')
def get_flickr_img_url(plant_name):
    """Gets link for flickr image and returns to angular."""

    url = get_flickr_image(plant_name)

    if url:
        return url
    else:
        return 'No image found.'


@app.route('/process_new_plant', methods=['POST'])
def process_new_plant():
    """Gets the user input from new plant form and adds to the database"""

    # if user did not add image url, get one from flickr
    name = request.form.get('name')
    image = request.form.get('image')
    if not image:
        image = get_flickr_image(name)

    # gets plant info from angular's data passed in and creates new Plant instance
    new_plant = Plant(name=name,
                      species=request.form.get('species'),
                      image=image,
                      water=request.form.get('water'),
                      sun=request.form.get('sun'),
                      humidity=request.form.get('humidity'),
                      temperature=request.form.get('temp'))

    # adds plant to the database and saves
    db.session.add(new_plant)
    db.session.commit()

    flash('Added plant!')

    # returns plant ID to angular's callback
    return str(new_plant.plant_id)


@app.route('/save_plant_edits', methods=['POST'])
def update_plant():
    """Updates plant"""

    plant = Plant.query.get(request.form.get('plant_id'))

    plant.name = request.form.get('name')
    plant.species = request.form.get('species')
    plant.image = request.form.get('image')
    plant.water = request.form.get('water')
    plant.sun = request.form.get('sun')
    plant.humidity = request.form.get('humidity')
    plant.temperature = request.form.get('temperature')

    print plant

    db.session.commit()

    return 'plant updated'


@app.route('/process_delete', methods=['POST'])
def process_delete():
    """Deletes plant from the database"""
    print '*' * 100
    print request.form.get('plant_id')
    plant_id = int(request.form.get('plant_id'))
    plant = Plant.query.get(plant_id)

    print plant.name + "deleting"
    db.session.delete(plant)
    db.session.commit()

    return 'Deleted.'


# **************************** HELPER FUNCTIONS *******************************

def get_reminder_status(user_id, plant_id):
    """Checks if PlantUser has an active reminder."""

    plant_user = PlantUser.query.filter(PlantUser.user_id == user_id, PlantUser.plant_id == plant_id).first()

    if plant_user.watering_schedule:
        return True
    else:
        return False


def get_user_plants(user_id):
    """Returns a list of plants a user has added."""

    user_plants = User.query.get(user_id).plants

    unpacked_user_plants = {}

    for plant in user_plants:
        unpacked_user_plants[plant.plant_id] = plant.__dict__

        if '_sa_instance_state' in unpacked_user_plants[plant.plant_id]:
            del unpacked_user_plants[plant.plant_id]['_sa_instance_state']

    return unpacked_user_plants


def get_all_users():
    return User.query.all()


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


def get_flickr_image(tag):
    """Get a random image from Flickr using the passed in term as a tag"""
    # tag = (tag + u', plant').encode('utf-8')
    r = flickr.photos.search(api_key=flickr_api_key, tags=tag.encode('utf-8'), format='json',
                             nojsoncallback=1, per_page=40)

    output = simplejson.loads(r)
    image_lst = output.items()[0][1]['photo']

    if len(image_lst) == 1:
        random_img = image_lst[0]
    elif len(image_lst) == 0:
        return ''
    else:
        random_img = image_lst[random.randint(0, len(image_lst)-1)]

    farm_id = random_img['farm']
    server_id = random_img['server']
    img_id = random_img['id']
    secret = random_img['secret']

    url = 'https://farm{}.staticflickr.com/{}/{}_{}.jpg'.format(farm_id, server_id, img_id, secret).encode('utf-8')

    return url


if __name__ == "__main__":

    connect_to_db(app)
    app.debug = True

    app.run(host="0.0.0.0")
