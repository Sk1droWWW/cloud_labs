from flask import request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from init import db_path
from init import db
from init import app

from petrol_enum import PetrolPriceUkraine
from car import Car


#ext
def loadSession():
    engine = create_engine(db_path, echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


#endpoints
@app.route('/cars/', methods = ['GET'])
def get_cars():
    session = loadSession()
    cars = session.query(Car).all()
   
    return jsonify([car.getJson() for car in cars])


@app.route('/cars/<id>/', methods=['GET'])
def get_car_by_id(id):
    session = loadSession()
    car = session.query(Car).filter_by(id=id).first()
   
    return jsonify([car.getJson()])


@app.route('/cars/', methods = ['POST'])
def create_car():
    session = loadSession()
    data = request.get_json()
    car = Car(
        name=data['name'],
        tank_capacity = data['tank_capacity'],
        petrol_quantity = data['petrol_quantity'],
        petrol_consumtion_per_100_km = data['petrol_consumtion_per_100_km'],
        petrol_type = data['petrol_type'],
    )

    session.add(car)
    session.commit()

    return jsonify([car.getJson()])


@app.route('/cars/<id>/', methods=['DELETE'])
def delete_car(id):
    session = loadSession()
    car = session.query(Car).filter_by(id=id).first()
    session.delete(car)
    session.commit()
    
    return {
		'success': 'Data deleted successfully'
	}


@app.route('/cars/<id>/', methods=['PUT'])
def update_сar(id):
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
    if 'petrol_type' in data: 
        car.petrol_type = data['petrol_type']
    
    session.add(car)
    session.commit()
	
    return jsonify([car.getJson()])


@app.route('/cars/fuel_cost/<id>/', methods=['GET'])
def calculate_fuel_cost(id):
    session = loadSession()
    data = request.get_json()

    car = session.query(Car).filter_by(id=id).first()
    
    km = data['km']
    price_per_litre = PetrolPriceUkraine[car.petrol_type].value
    petrol_total = car.petrol_consumtion_per_100_km * km / 100

    price_total = petrol_total * price_per_litre

    return {
		'price_total': price_total
	}
  

#main
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=80)