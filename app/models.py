from enum import unique
from sqlalchemy.orm import backref, relationship
from app import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from app import login
import datetime



class User(UserMixin, db.Model):
    __bind_key__ = 'User' 
    id = db.Column(db.Integer, unique=True, primary_key=True)
    Phone_Number = db.Column(db.String(30), unique=True, nullable=False)
    fname= db.Column(db.String(15), unique=False, nullable=False)
    lname = db.Column(db.String(15), unique=False, nullable=False)
    gender = db.Column(db.String(7), unique=False, nullable=False)
    dob = db.Column(db.String(10), unique=False, nullable=False)
    passhash = db.Column(db.String(180), unique=False, nullable=False)
    providence_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    reviews = db.relationship('UserReviews', backref = 'user', lazy=True)
    

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class UserReviews(db.Model):
    __bind_key__= 'UserReviews'
    review_id = db.Column(db.Integer, Primary_key=True, AutoIncrement=True, nullable =False )
    reviews_content = db.Column(db.String(500), unique=False, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

class Providence(db.Model):
    __bind_key__ = 'Providence' 
    Providence=db.Column(db.String(50), unique=False, nullable=False)
    id = db.Column(db.Integer, unique=True, primary_key=True)
    GPS = db.Column(db.String(30), unique=True, nullable=False)
    Town= db.Column(db.String(15), unique=False, nullable=False)
    Town_GPS= db.Column(db.String(50), unique=True, nullable=False)
    Landmarks = db.Column(db.String(30), unique=False, nullable=False)
    Landmarks_GPS = db.Column(db.String(10), unique=True, nullable=False)
    BusStop = db.Column(db.String(30), unique=False, nullable=False)
    BusStop_GPS = db.Column(db.String(50), unique=True, nullable=False)
    Stations=db.Column(db.String(30), unique=False, nullable=False)
    Stations_GPS=db.Column(db.String(50), unique=True, nullable=False)


class Stations(db.Model):
    __bind_key__ = 'Stations' 
    id = db.Column(db.Integer, unique=True, primary_key=True)
    Station_Name = db.Column(db.String(30), unique=False, nullable=False)
    Station_GPS = db.relationship('Providence', backref = 'Station_GPS', lazy=True)
    Working_HRS=db.Column(db.String, unique=False, nullable=False)
    Station_Master_id=db.relationship('StationMaster', backref='id', lazy=True)
    CarsWorking=db.Column(db.Integer, unique=False, nullable=False)
    Station_Contact=db.Column(db.Integer, unique=True, nullable=False)
    Destinations=db.Column(db.String(50), unique=False, nullable=False)
    Destinations_GPS=db.Column(db.String(50), unique=False, nullable=False)

class Trotromates(db.Model):
    __bind_key__ = 'Trotromates' 
    id = db.Column(db.Integer, unique=True, primary_key=True)
    Phone_Number = db.Column(db.String(30), unique=True, nullable=False)
    fname= db.Column(db.String(15), unique=False, nullable=False)
    lname = db.Column(db.String(15), unique=False, nullable=False)
    gender = db.Column(db.String(7), unique=False, nullable=False)
    station_id = db.relationship('Stations',backref ='station.id', lazy=True)



class Drivers(db.Model):
    __bind_key__ = 'Drivers' 
    id = db.Column(db.Integer, unique=True, primary_key=True)
    Phone_Number = db.Column(db.String(30), unique=True, nullable=False)
    fname= db.Column(db.String(15), unique=False, nullable=False)
    lname = db.Column(db.String(15), unique=False, nullable=False)
    gender = db.Column(db.String(7), unique=False, nullable=False)
    station_id = db.relationship('Stations',backref ='station.id', lazy=True)
    GHcard=db.Column(db.String(20), unique=True, nullable=False)

class StationMaster(db.Model):
    __bind_key__ = 'StationMaster' 
    id = db.Column(db.Integer, unique=True, primary_key=True)
    Phone_Number = db.Column(db.String(30), unique=True, nullable=False)
    fname= db.Column(db.String(15), unique=False, nullable=False)
    lname = db.Column(db.String(15), unique=False, nullable=False)
    gender = db.Column(db.String(7), unique=False, nullable=False)
    station_id = db.relationship('Stations',backref ='station.id', lazy=True)
    GHcard=db.Column(db.String(20), unique=True, nullable=False)

class Agents(db.Model):
    __bind_key__ = 'Agents' 
    id = db.Column(db.Integer, unique=True, primary_key=True)
    Phone_Number = db.Column(db.String(30), unique=True, nullable=False)
    fname= db.Column(db.String(15), unique=False, nullable=False)
    lname = db.Column(db.String(15), unique=False, nullable=False)
    gender = db.Column(db.String(7), unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    GHcard=db.Column(db.String(20), unique=True, nullable=False)

class CarsOwners(db.Model):
    __bind_key__ = 'Agents' 
    id = db.Column(db.Integer, unique=True, primary_key=True)
    Phone_Number = db.Column(db.String(30), unique=True, nullable=False)
    fname= db.Column(db.String(15), unique=False, nullable=False)
    lname = db.Column(db.String(15), unique=False, nullable=False)
    gender = db.Column(db.String(7), unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    GHcard=db.Column(db.String(20), unique=True, nullable=False)

class ForSale(db.Model):
    __bind_key__='ForSale'
    id= db.Column(db.Integer, unique=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    carplate=db.Column(db.Integer, unique=True, primary_key=True)
    car_des=db.Column(db.String(100), unique=True, primary_key=True)
    created_posted=db.Column(DateTime, default=datetime.datetime.utcnow)

