# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()


####################################################################
# Model definitions


class Plant(db.Model):
    """Plant. A plant has many users"""

    __tablename__ = "plants"

    plant_id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(264))
    name = db.Column(db.String(64), nullable=False)
    species = db.Column(db.String(64))
    water = db.Column(db.Integer)
    sun = db.Column(db.Integer)
    soil = db.Column(db.String(32))
    misc = db.Column(db.UnicodeText)

    def __repr__(self):
        return "<{}, {}.>".format(self.name.encode('utf-8').strip(), self.species.encode('utf-8').strip())


class User(db.Model):
    """User. A user has many plants."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), nullable=False, unique=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(32), nullable=False)

    def __repr__(self):
        return "<{} ({}).>".format(self.username, self.email)


class PlantUser(db.Model):
    """An association table for user plants"""

    userplant_id = db.Column(db.Integer, primary_key=True)
    plant_id = db.Column(db.Integer, db.ForeignKey('plants.plant_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    plants = db.relationship('Plant', backref='plantusers')
    users = db.relationship('User', backref='plantusers')


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
        # Plant(name='Baby Donkey Tail',
        #       species='Succulent',
        #       image="http://worldofsucculents.com/wp-content/uploads/2013/09/Sedum-burrito-Burro’s-Tail-Baby-Donkey-Tail1.jpg",
        #       water=3,
        #       sun=3)
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
    db.create_all()
    #example_data()

    print "Connected to DB."
