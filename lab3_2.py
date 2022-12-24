import os
from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import mapper, sessionmaker

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
   
    return session.query(Car).all()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=80)