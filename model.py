# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from twilio.rest import TwilioRestClient
import schedule
import secret
import time
import json

db = SQLAlchemy()


####################################################################
# Model definitions

class Plant(db.Model):
    """Plant. A plant has many users"""

    __tablename__ = "plants"

    plant_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image = db.Column(db.String(264))
    name = db.Column(db.String(64), nullable=False, unique=True)
    species = db.Column(db.String(64))
    water = db.Column(db.String(128))
    sun = db.Column(db.String(128))
    humidity = db.Column(db.String(128))
    temperature = db.Column(db.String(128))
    misc = db.Column(db.UnicodeText)

    users = db.relationship("User", secondary="plant_users", backref="plants")

    def get_water_specs():
        """Get water json."""

        with open('static/data/specs/water_specs.json') as data_file:
            data = json.load(data_file)
        return data

    def get_sun_specs():
        """Get sun json."""

        with open('static/data/specs/sun_specs.json') as data_file:
            data = json.load(data_file)
        return data

    def get_humid_specs():
        """Get sun json."""

        with open('static/data/specs/humidity_specs.json') as data_file:
            data = json.load(data_file)
        return data

    def get_temp_specs():
        """Get sun json."""

        with open('static/data/specs/temp_specs.json') as data_file:
            data = json.load(data_file)
        return data

    WATER = get_water_specs()
    SUN = get_sun_specs()
    HUMIDITY = get_humid_specs()
    TEMPERATURE = get_temp_specs()

    def get_sun(self, key='description'):
        """For a specific plant, returns the sun information"""
        if self.sun:
            return Plant.SUN[self.sun][key]

    def get_water(self, key='description'):
        """For a specific plant, returns the water information"""
        if self.water:
            return Plant.WATER[self.water][key]

    def get_temp(self, key='description'):
        """For a specific plant, returns the temperature information"""
        if self.temperature:
            return Plant.TEMPERATURE[self.temperature][key]

    def get_humidity(self, key='description'):
        """For a specific plant, returns the humidity information"""
        if self.humidity:
            return Plant.HUMIDITY[self.humidity][key]

    # def __repr__(self):
    #     return "<{}, {}.>".format(self.name.encode('utf-8').strip(), self.species.encode('utf-8').strip())


class User(db.Model):
    """User. A user has many plants."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # User authentication information
    username = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.Integer, nullable=False, server_default='')

    # User email information
    email = db.Column(db.String(255), nullable=False, unique=True)
    confirmed_at = db.Column(db.DateTime())

    # User information
    first_name = db.Column(db.String(100), nullable=False, server_default='')
    last_name = db.Column(db.String(100), nullable=False, server_default='')
    image = db.Column(db.String(264), server_default='https://medium.com/img/default-avatar.png')


class PlantUser(db.Model):
    """An association table for user plants"""

    __tablename__ = "plant_users"

    userplant_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    plant_id = db.Column(db.Integer, db.ForeignKey('plants.plant_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))


def example_data():
    """Create some sample data."""

    # convert json file into dictionary
    with open('static/data/plant_results_with_child_nodes.json') as data_file:
        data = json.load(data_file)

    for plant in data:
        if plant['name'] and plant['species']:

            plants_411 = [
                Plant(name=plant['name'][0].encode('utf-8').strip(),
                      species=plant['species'][0].encode('utf-8').strip(),
                      misc=plant['value'][0].encode('utf-8').strip())
            ]
            db.session.add_all(plants_411)

    test_plants = [
        Plant(name='Baby Donkey Tail',
              species='Succulent',
              image="http://worldofsucculents.com/wp-content/uploads/2013/09/Sedum-burrito-Burro’s-Tail-Baby-Donkey-Tail1.jpg",
              water="Moderately Moist",
              sun="Bright Light")
    ]

    db.session.commit()


class Reminder():
    """Schedules and sends SMS reminders."""

    account_sid = secret.TWILIO_SID
    auth_token = secret.TWILIO_AUTH
    client = TwilioRestClient(account_sid, auth_token)

    def __init__(self, number, days, plant):
        self.number = number
        self.days = days
        self.plant = plant

    # set up a client to talk to the Twilio REST API

    def send_sms(self, msg='testing ¯\_(ツ)_/¯'):

        message = self.client.messages.create(
            to=self.number,
            from_="+16506678554",
            body="It's time to water your {}!".format(self.plant)
        )
        print(message.sid)

    def schedule_test(self):
        schedule.every(30).seconds.do(self.send_sms)
        # for day in self.days:
        #     schedule.every().wednesday.at("9:00").do(self.send_sms)
        counter = 0
        while True:
            print counter
            schedule.run_pending()
            time.sleep(1)
            counter += 1

        # schedule.every(5).seconds.do(self.send_sms())
        # schedule.every().hour.do(job)
        # schedule.every().day.at("10:30").do(job)
        # schedule.every().monday.do(job)
        # schedule.every().wednesday.at("13:15").do(job)

####################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to the Flask app."""

    # Configure to use our database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///plants'
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    from server import app
    connect_to_db(app)

    # Create our tables and some sample data
    # db.create_all()
    # example_data()

    print "Connected to DB."
