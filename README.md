#  🌱 planty  [![Build Status](https://travis-ci.org/agnaite/planty.svg?branch=master)](https://travis-ci.org/agnaite/planty)

Planty takes the mystery out of keeping plants alive! Intended for both the novice and the seasoned professional, this app provides concise, user-friendly guidance on how to take care of houseplants. Users can search for plants by name or plant profile, add new plants to the database, edit current plants, and schedule watering reminders for plants they own.

## Table of Contents

* [Tech Stack](#tech-stack)
* [Features](#features)
* [Setup/Installation](#installation)
* [Version 2.0](#future)
* [License](#license)

## <a name="tech-stack"></a>Tech Stack

__Frontend:__ HTML5, Sass, AngularJS, Javascript, jQuery, Bootstrap <br/>
__Backend:__ Python, Flask, PostgreSQL, SQLAlchemy, Scrapy <br/>
__APIs:__ Flickr, Twilio <br/>

## <a name="features"></a>Features

#### Search for plants by name, water, sun, temperature, or humidity needs. User account registration not required.
  
![Plant Search Logged out](/static/img/_readme-img/search-loggedout.gif)

#### Register or login to edit a plant.
  
![Edit Plant](/static/img/_readme-img/edit-plant.gif)

#### Add and remove plants from your account.
  
![Add Plant](/static/img/_readme-img/adding-plant.gif)

#### Schedule watering reminders for your plants.
  
![Schedule Reminder](/static/img/_readme-img/scheduling-reminder.gif)

## <a name="installation"></a>Setup/Installation

To have this app running on your local computer, please follow the below steps:

####Requirements:

- Install PostgreSQL
- Python 2.7
- Flickr and Twilio API keys

Clone repository:
```
$ git clone https://github.com/agnaite/planty.git
```
Create a virtual environment:
```
$ virtualenv env
```
Activate the virtual environment.
```
$ source env/bin/activate
```
Install dependencies.
```
$ pip install -r requirements.txt
```
Get your own secret keys for [Flickr](http://developer.etsy.com) and [Twilio](www.ebay.com). Save them to a file <kbd>secrets.py</kbd>. Your file should look something like this:
```
APP_KEY = 'xyz'
FLICKR_API_KEY = 'abc'
FLICKR_API_SECRET = 'abc'
TWILIO_SID = 'abc'
TWILIO_AUTH = 'abc'
```
Create database 'plants'.
```
$ createdb plants
```
Create your database tables and seed example data.
```
$ python model.py
```
Run the app from the command line.
```
$ python server.py
```
If you want to use SQLAlchemy to query the database, run in interactive mode
```
$ python -i model.py
```

## <a name="future"></a>Version 2.0

## <a name="license"></a>License

The MIT License (MIT)
Copyright (c) 2016 Agne Klimaite 

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
