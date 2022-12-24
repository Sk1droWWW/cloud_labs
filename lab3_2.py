import os
from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import json
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.ext.declarative import DeclarativeMeta

class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)



app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# db models
class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    tank_capacity = db.Column(db.Integer, nullable=False)
    petrol_quantity = db.Column(db.Integer, nullable=False)
    petrol_consumtion_per_100_km = db.Column(db.Integer, nullable=False)

    def __init__(self, name, tank_capacity, petrol_quantity, petrol_consumtion_per_100_km):
        self.name = name
        self.tank_capacity = tank_capacity
        self.petrol_quantity = petrol_quantity
        self.petrol_consumtion_per_100_km = petrol_consumtion_per_100_km

    def __repr__(self):
        return "Car {}".format(self.name)


def loadSession():
    engine = create_engine(db_path, echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

@app.route('/cars', methods = ['GET', 'POST'])
def new():
    session = loadSession()

    if request.method == 'POST':
        car = Car(request.form['name'], request.form['tank_capacity'],
            request.form['petrol_quantity'], request.form['petrol_consumtion_per_100_km'])
        
        session.add(car)
        session.commit()
    
    cars = session.query(Car).all()
   
    return json.dumps(cars, cls=AlchemyEncoder)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=80)