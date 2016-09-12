# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
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


class User(db.Model):
    """User. A user has many plants."""

    __tablename__ = "users"

    user_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)

    # User authentication information
    username = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    # User email information
    email = db.Column(db.String(255), nullable=False, unique=True)
    confirmed_at = db.Column(db.DateTime())

    # User information
    first_name = db.Column(db.String(100), nullable=False, server_default='')
    last_name = db.Column(db.String(100), nullable=False, server_default='')
    image = db.Column(db.String(264), server_default='https://medium.com/img/default-avatar.png')
    phone = db.Column(db.String(128), unique=True)


class PlantUser(db.Model):
    """An association table for user plants"""

    __tablename__ = "plant_users"

    userplant_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    plant_id = db.Column(db.Integer, db.ForeignKey('plants.plant_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    watering_schedule = db.Column(db.String(128))

    def get_watering_days(self):
        if self.watering_schedule:
            return self.watering_schedule.split(',')
        else:
            return []


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

    db.session.commit()


####################################################################
# Helper functions


def connect_to_db(app, db_uri=None):
    """Connect the database to the Flask app."""

    # Configure to use our database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri or 'postgresql:///plants'

    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    from server import app
    import os
    connect_to_db(app, os.getenv('DATABASE_URL'))

    # Create our tables and some sample data
    db.create_all()
    example_data()

    print "Connected to DB."
