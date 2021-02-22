from Flask_Cinema_Site import db
from datetime import datetime
from flask_login import UserMixin


class Customer(db.Model, UserMixin):
    __tablename__ = "customer"
    customerid = db.Column(db.Integer, unique=True,
                           primary_key=True, autoincrement=True)
    email = db.Column(db.String(70), unique=True, nullable=False)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    customerViewingLinks = db.relationship('CustomerViewingLink',
                                           backref='Customer', lazy=True)
    basket = db.relationship('Basket',
                             backref='Customer', lazy=True)

    def get_id(self):
        return (self.customerid)


class CustomerViewingLink(db.Model):
    __tablename__ = "customerViewingLink"
    transactionid = db.Column(db.Integer, unique=True,
                              primary_key=True)
    customerid = db.Column(db.Integer, db.ForeignKey('customer.customerid'),
                           unique=True,
                           primary_key=True)
    viewingid = db.Column(db.Integer, db.ForeignKey('viewing.viewingid'),
                          unique=True,
                          primary_key=True)


class Basket(db.Model):
    __tablename__ = "basket"
    customerid = db.Column(db.Integer, db.ForeignKey('customer.customerid'),
                           unique=True,
                           primary_key=True)
    basketviewinglinks = db.relationship('BasketViewingLink',
                                         backref='Customer', lazy=True)


class BasketViewingLink(db.Model):
    __tablename__ = "basketviewinglink"
    customerid = db.Column(db.Integer, db.ForeignKey('customer.customerid'),
                           unique=True,
                           primary_key=True)
    viewingid = db.Column(db.Integer, db.ForeignKey('viewing.viewingid'),
                          unique=True,
                          primary_key=True)


class Viewing(db.Model):
    __tablename__ = "viewing"
    viewingid = db.Column(db.Integer, unique=True,
                          primary_key=True)
    movieid = db.Column(db.Integer, db.ForeignKey('movie.movieid'),
                        unique=True)
    customerViewingLinks = db.relationship('CustomerViewingLink',
                                           backref='Viewing', lazy=True)
    basketviewinglink = db.relationship('BasketViewingLink',
                                        backref='Customer', lazy=True)


class Movie(db.Model):
    __tablename__ = "movie"
    movieid = db.Column(db.Integer, unique=True,
                        primary_key=True)
    viewings = db.relationship('viewing',
                               backref='movie', lazy=True)


class ViewingSeatLink(db.Model):
    __tablename__ = "viewingseatlink"
    seatid = db.Column(db.Integer, unique=True,
                       primary_key=True)
    viewingid = db.Column(db.Integer, unique=True,
                          primary_key=True)


class Seat(db.Model):
    __tablename__ = "seat"
    seatid = db.Column(db.Integer, unique=True,
                       primary_key=True)
    theatreid = db.Column(db.Integer, db.ForeignKey('theatre.theatreid'),
                          unique=True,
                          primary_key=True)
    theatre = db.relationship('Theatre',
                              backref='seat', lazy=True)


class Theatre(db.Model):
    __tablename__ = "theatre"
    theatreid = db.Column(db.Integer, unique=True,
                          primary_key=True)
    seatid = db.Column(db.Integer, db.ForeignKey('seat.seatid'),
                       unique=True)
    seats = db.relationship('seat',
                            backref='theatre', lazy=True)
