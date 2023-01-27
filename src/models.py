from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    likes = db.relationship('Likes', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' %self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "password": self.password,
        }

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    birth_year = db.Column(db.String(250))
    gender = db.Column(db.String(250), nullable=False)
    eye_color = db.Column(db.String(250), nullable=False)
    likes = db.relationship('Likes', backref='people', lazy=True)

    def __repr__(self):
        return '<People %r>' %self.id

    def serialize(self):
        return {
            "id":self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "eye_color": self.eye_color,

        }

class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    population = db.Column(db.String(250))
    gravity = db.Column(db.String(250), nullable=False)
    climate = db.Column(db.String(250), nullable=False)
    likes = db.relationship('Likes', backref='planets', lazy=True)

    def __repr__(self):
        return '<Planets %r>' %self.id

    def serialize(self):
        return {
            "name": self.name,
            "population": self.population,
            "gravity": self.gravity,
            "climate": self.climate,

        }

class Vehicles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    model = db.Column(db.String(250))
    vehicle_class = db.Column(db.String(250), nullable=False)
    passengers = db.Column(db.String(250), nullable=False)
    likes = db.relationship('Likes', backref='vehicles', lazy=True)

    def __repr__(self):
        return '<Vehicles %r>' %self.id

    def serialize(self):
        return {
            "name": self.name,
            "model": self.model,
            "vehicle_class": self.vehicle_class,
            "passengers": self.passengers,

        }

#         class Person(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), nullable=False)
#     addresses = db.relationship('Address', backref='person', lazy=True)

# class Address(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), nullable=False)
#     person_id = db.Column(db.Integer, db.ForeignKey('person.id'),
#         nullable=False)

class Likes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'))
    planets_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    vehicles_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Likes %r>' %self.id

    def serialize(self):
        return {
            "people_id": self.people_id,
            "planets_id": self.planets_id,
            "vehicles_id": self.vehicles_id,
            "user_id": self.user_id,

        }


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(80), unique=False, nullable=False)
#     is_active = db.Column(db.Boolean(), unique=False, nullable=False)

#     def __repr__(self):
#         return '<User %r>' % self.username

#     def serialize(self):
#         return {
#             "id": self.id,
#             "email": self.email,
#             # do not serialize the password, its a security breach
#         }