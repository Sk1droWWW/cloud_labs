import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# create the extension
# create the app
db = SQLAlchemy()
app = Flask(__name__)

# configure the SQLite database, relative to the app instance folder
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')# initialize the app with the extension
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)



# endpoints
@app.route('/')
def index():
    return 'Web App with Python Flask by Mykhailo'



# db models
class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    tank_capacity = db.Column(db.Integer, nullable=False)
    petrol_quantity = db.Column(db.Integer, nullable=False)
    petrol_consumtion = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "Car {}".format(self.name)



# run
app.run(host='0.0.0.0', port=80)