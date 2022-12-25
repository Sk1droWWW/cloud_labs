from init import db

# db models
class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    tank_capacity = db.Column(db.Integer, nullable=False)
    petrol_quantity = db.Column(db.Integer, nullable=False)
    petrol_consumtion_per_100_km = db.Column(db.Integer, nullable=False)
    petrol_type = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return "Car {}".format(self.name)

    def getJson(self):
        return {
                'id': self.id, 
                'name': self.name,
                'tank_capacity': self.tank_capacity,
                'petrol_quantity': self.petrol_quantity,
                'petrol_consumtion_per_100_km': self.petrol_consumtion_per_100_km,
                'petrol_type': self.petrol_type
            } 
