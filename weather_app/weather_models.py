from weather_app import db

class City(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    city_name = db.Column(db.String(30), unique = True, nullable = False)