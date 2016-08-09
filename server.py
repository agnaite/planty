# -*- coding: utf-8 -*-

from flask import Flask, render_template
from model import connect_to_db, db, Plant, User, PlantUser
import secret

app = Flask(__name__)
app.secret_key = secret.APP_KEY


@app.route('/')
def index_page():
    """Show index page."""
    print "hey"
    return render_template("index.html")


@app.route('/all_plants')
def show_all_plants_by_name():
    """Show all plants by name."""

    print "\n\n\n\n\nSTARTED QUERY\n\n"
    all_plants = Plant.query.all()
    print "\n\n\nFINISHED QUERY\n\n"

    return render_template("plants_by_name.html", plants=all_plants)


if __name__ == "__main__":

    connect_to_db(app)
    app.debug = True

    app.run(host="0.0.0.0")
