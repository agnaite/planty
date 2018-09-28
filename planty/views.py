# -*- coding: utf-8 -*-
from flask import request, render_template, \
                  jsonify, session, redirect, url_for
import sys
import os
import simplejson
import random
import flickrapi 
from datetime import datetime
import bcrypt

from planty.models import db, Plant, User, PlantUser
from planty import app
from planty import reminder_sender

flickr = flickrapi.FlickrAPI(app.config['FLICKR_API_KEY'], app.config['FLICKR_API_SECRET'])

# Basic Routes *********************************

@app.route('/')
def index_page():
    """Show index page."""
    return render_template("base.html")


@app.route('/html_for_angular/<filename>')
def html_for_angular(filename):
    """Sends html to angular."""
    return render_template('angular/{}'.format(filename))


@app.route('/search', methods=['POST'])
def search_for_plant():
    """Retrieves search results from database."""
    search_term = request.form.get('name')
    filters = '&' + request.form.get('filters')
    filters = filters.replace('%20', " ").split('&')[1:]

    # make dict out of the unicode string passed from angular
    filter_results = []

    if filters[1:]:
        for filter in filters:
            filter = filter.split('=')
            if filter[1] == 'water':
                results = Plant.query.filter(Plant.water == filter[0]).all()
                filter_results.extend(results)
            elif filter[1] == 'sun':
                results = Plant.query.filter(Plant.sun == filter[0]).all()
                filter_results.extend(results)
            elif filter[1] == 'temp':
                results = Plant.query.filter(Plant.temperature == filter[0]).all()
                filter_results.extend(results)
            else:
                results = Plant.query.filter(Plant.humidity == filter[0]).all()
                filter_results.extend(results)

    if search_term.strip() == '' and filter_results == []:
        return 'None'
    elif search_term.strip() == '':
        results = Plant.query.all()
    else:
        # gets the user's search term from app.js and queries the db
        results = Plant.query.filter(Plant.name.ilike('%' + search_term + '%')).all()

    if filter_results:
        results = list(set(results).intersection(filter_results))

    plants_found = {}

    if results:
        # for each plant in the results, make dictionary using plant's id as key
        # and plant's other data as value
        for plant in results:
            plants_found[plant.plant_id] = {'id': plant.plant_id,
                                            'name': plant.name}

    if plants_found:
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

    # adds a key to dictionary that has a value of true/false depending on
    # whether reminder was set
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


@app.route('/is_phone_number/<phone>')
def check_if_phone_is_taken(phone):
    """Checks if a phone number is already in the database"""
    user = User.query.filter_by(phone=phone).first()

    if user:
        return "True"
    else:
        return "False"


@app.route('/get_profile_img', methods=['POST'])
def retrieve_user_image():
    """Gets the profile image of the current user."""
    user = User.query.get(request.form.get('user_id'))
    return user.image


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
    """Processes user input and logs user in, if user exists and has the correct password."""

    # gets the user input from the username field and looks it up in the database
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()

    # if username entered exists in db, gets the password entered and compares
    # it to the one in the database
    if user:
        # if password is correct, adds user to the current session and redirects to home page
        if bcrypt.hashpw(request.form.get('password').encode('utf-8'), user.password.encode('utf-8')).decode() == user.password:
            session['logged_in'] = user.user_id
            response = {'logged_in': user.user_id}
            return jsonify(response)
        # if password is incorrect, redirects to login page
        # TODO: differentiate between the two errors below
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
                    password=bcrypt.hashpw(request.form.get('password').encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                    email=request.form.get('email'),
                    image=request.form.get('image'),
                    phone=request.form.get('phone'),
                    confirmed_at=datetime.now())

    # adds the new user instance to the database and saves
    db.session.add(new_user)
    db.session.commit()

    # logs new user in
    session['logged_in'] = new_user.user_id
    new_user = new_user.__dict__

    if '_sa_instance_state' in new_user:
        del new_user['_sa_instance_state']

    # passes new user's id to angular
    new_user['logged_in'] = session['logged_in']

    return jsonify(new_user)


@app.route('/process_user_update', methods=['POST'])
def update_user():
    """Saves updated user info."""
    user_id = request.form.get('id')
    user_to_update = User.query.get(int(user_id))

    if bcrypt.hashpw(request.form.get('password').encode('utf-8'), user_to_update.password.encode('utf-8')).decode() == user_to_update.password:
        if request.form.get('email'):
            user_to_update.email = request.form.get('email')
        if request.form.get('phone'):
            user_to_update.phone = request.form.get('phone')
    else:
        return "bad password"

    db.session.commit()

    return "ok"


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

    if user.plants and plant in user.plants:
        return 'true'
    else:
        return 'false'


@app.route('/process_new_reminder', methods=['POST'])
def add_reminder():
    """Adds a watering reminder for a particular PlantUser"""
    user_id = int(request.form.getlist('user_id')[0])

    if User.query.get(user_id).phone:
        plant_id = int(request.form.getlist('plant_id')[0])
        days = request.form.getlist('days')[0]

        plant_user = PlantUser.query.filter(PlantUser.user_id == user_id, PlantUser.plant_id == plant_id).first()
        plant_user.watering_schedule = days

        db.session.commit()

        return 'ok'
    else:
        return 'phone number missing'


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

    db.session.commit()

    return 'plant updated'


@app.route('/process_delete', methods=['POST'])
def process_delete():
    """Deletes plant from the database"""
    plant_id = int(request.form.get('plant_id'))
    plant = Plant.query.get(plant_id)

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
    r = flickr.photos.search(api_key=app.config['FLICKR_API_KEY'], tags=tag.encode('utf-8'), format='json',
                             nojsoncallback=1, per_page=40)

    output = simplejson.loads(r)

    image_lst = list(output.items())[0][1]['photo']

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

    url = "https://farm{}.staticflickr.com/{}/{}_{}.jpg".format(farm_id, server_id, img_id, secret)

    return url


if __name__ == "__main__":

    connect_to_db(app, os.environ.get("DATABASE_URL"))
    # app.debug = False

    DEBUG = "NO_DEBUG" not in os.environ

    PORT = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)
