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
    name = db.Column(db.String(64), nullable=False)
    species = db.Column(db.String(64))
    water = db.Column(db.String(128))
    sun = db.Column(db.String(128))
    humidity = db.Column(db.String(128))
    temperature = db.Column(db.String(128))
    misc = db.Column(db.UnicodeText)

    users = db.relationship("User", secondary="plant_users", backref="plants")

    WATER = {
        "Moderately Moist": {'description': "Water thoroughly as soon as its potting mix begins to dry out. Cannot tolerate drought.",
                             'icon': ''},
        "Drench and Let Dry": {'description': "During potting season, water as soon as its potting mix begins to dry out. When not in a phase of rapid growth, water thoroughly, but allow mix to become dry for a day or two before watering again. Never allow plant to wilt.",
                               'icon': ''},
        "Keep on the Dry Side": {'description': "Water thoroughly during growing season. Let mix go until it is dry to the touch. If plant is completely dormant, it needs no water at all for a lengthy period.",
                                 'icon': ''}
    }
    SUN = {
        "Full Sun": {'description': "Full sun at least four hours a day. Bright light the rest of the day.",
                     'icon': ''},
        "Bright Light": {'description': "Fewer than four hours of direct sun a day. Intense light for eight or more.",
                         'icon': ''},
        "Medium Light": {'description': "Prefer good light. Little direct sun, except perhaps in the morning or late afternoon.",
                         'icon': ''},
        "Low Light": {'description': "Prefer moderate to weak light with no direct sun.",
                      'icon': ''}
    }
    HUMIDITY = {
        "High Humidity": {'description': "Plants do best in a very humid environment where a home humidifying system is installed.",
                          'icon': ''},
        "Moderate Humidity": {'description': "Grow best in a humid room. Some sort of humidifying system is often required.",
                              'icon': ''},
        "Average Home Humidity": {'description': "Can tolerate dry air.",
                                  'icon': ''},
        "Good Air Circulation": {'description': "Can tolerate stagnant air.",
                                 'icon': ''}
    }
    TEMPERATURE = {
        "Normal Room Temperatures": {'description': "Tolerate normal room temperatures year-around, from 65F to 75F (18C to 24C).",
                                     'icon': ''},
        "Warm Temperatures": {'description': "Tolerate normal room temperatures very well during warmer months, but do not like temperatures below 65F (18C). No air conditioning.",
                              'icon': ''},
        "Cool Temperatures": {'description': "Tolerate normal room temperatures during their growing period, but like cooler temperatures, around 45F to 55F (7C to 13C), during their rest period.",
                              'icon': ''},
        "Cold Temperatures": {'description': "Prefer cold temperatures - 35F to 45F (2C - 7C). Never expose to freezing temperatures.",
                              'icon': ''}
    }

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
    username = db.Column(db.String(16), nullable=False, unique=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(32), nullable=False)

    # def __repr__(self):
    #     return "<{} ({}).>".format(self.username, self.email)


class PlantUser(db.Model):
    """An association table for user plants"""

    __tablename__ = "plant_users"

    userplant_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    plant_id = db.Column(db.Integer, db.ForeignKey('plants.plant_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))


def example_data():
    """Create some sample data."""

    # convert json file into dictionary
    with open('data/plant_results_with_child_nodes.json') as data_file:
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
