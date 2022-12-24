import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#init
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

    def __repr__(self):
        return "Car {}".format(self.name)

#ext
def loadSession():
    engine = create_engine(db_path, echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

#endpoints
@app.route('/cars/', methods = ['GET'])
def get_cars_jsonify():
    session = loadSession()
    cars = session.query(Car).all()
   
    return jsonify([getCarJson(car) for car in cars])


@app.route('/cars/', methods = ['POST'])
def create_car():
    session = loadSession()
    data = request.get_json()
    car = Car(
        name=data['name'],
        tank_capacity = data['tank_capacity'],
        petrol_quantity = data['petrol_quantity'],
        petrol_consumtion_per_100_km = data['petrol_consumtion_per_100_km'],
    )

    session.add(car)
    session.commit()

    return jsonify([getCarJson(car)])


@app.route('/cars/<id>/', methods=['DELETE'])
def delete_user(id):
    session = loadSession()
    car = session.query(Car).filter_by(id=id).first()
    session.delete(car)
    session.commit()
    
    return {
		'success': 'Data deleted successfully'
	}


@app.route('/cars/<id>/', methods=['PUT'])
def update_user(id):
    session = loadSession()
    data = request.get_json()
    
    car = session.query(Car).filter_by(id=id).first()
    if 'name' in data: 
        car.name = data['name']
    if 'tank_capacity' in data: 
        car.tank_capacity = data['tank_capacity']
    if 'petrol_quantity' in data: 
        car.petrol_quantity = data['petrol_quantity']
    if 'petrol_consumtion_per_100_km' in data: 
        car.petrol_consumtion_per_100_km = data['petrol_consumtion_per_100_km']
    
    session.add(car)
    session.commit()
	
    return jsonify([getCarJson(car)])

#endpoint ext
def getCarJson(car):
    return {
			'id': car.id, 
            'name': car.name,
            'tank_capacity': car.tank_capacity,
            'petrol_quantity': car.petrol_quantity,
			'petrol_consumtion_per_100_km': car.petrol_consumtion_per_100_km
        } 

#main
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=80)