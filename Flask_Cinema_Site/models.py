from Flask_Cinema_Site import db
from datetime import datetime
from flask_login import UserMixin
from time import time
import jwt
from Flask_Cinema_Site import app


class Customer(db.Model, UserMixin):
    __tablename__ = "customer"
    id = db.Column(db.Integer, primary_key=True)

    customer_viewings = db.relationship('CustomerViewing', backref='customer', lazy=True)
    basket = db.relationship('Basket', backref='customer', lazy=True)

    # Data fields
    email = db.Column(db.String(70), nullable=False, unique=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    confirmed = db.Column(db.Boolean, nullable=False, default=False)

    def get_reset_password_token(self, expires_in=86400):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except jwt.ExpiredSignatureError:
            return
        except jwt.DecodeError:
            return
        except jwt.InvalidTokenError:
            return
        return Customer.query.get(id)


class CustomerViewing(db.Model):
    __tablename__ = "customer_viewing"
    transaction_id = db.Column(db.Integer, unique=True, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), unique=True, primary_key=True)
    viewing_id = db.Column(db.Integer, db.ForeignKey('viewing.id'), unique=True, primary_key=True)


class Basket(db.Model):
    __tablename__ = "basket"
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), unique=True, primary_key=True)
    basket_viewing = db.relationship('BasketViewing', backref='basket', lazy=True)


class BasketViewing(db.Model):
    __tablename__ = "basket_viewing"
    customer_basket_id = db.Column(db.Integer, db.ForeignKey('basket.customer_id'), unique=True,
                                   primary_key=True)
    viewing_id = db.Column(db.Integer, db.ForeignKey('viewing.id'), unique=True, primary_key=True)


class Viewing(db.Model):
    __tablename__ = "viewing"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    time = db.Column(db.DateTime, nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), unique=True)

    customer_viewings = db.relationship('CustomerViewing', backref='viewing', lazy=True)
    basket_viewing = db.relationship('BasketViewing', backref='customer', lazy=True)


class Movie(db.Model):
    __tablename__ = "movie"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    viewings = db.relationship('Viewing', backref='movie', lazy=True)

    # Data fields
    # TODO Fix string lengths
    name = db.Column(db.String(100), nullable=False)
    overview = db.Column(db.String(250), nullable=False)
    released = db.Column(db.Date, nullable=False)

    cover_art_name = db.Column(db.String(35), nullable=False)

    # Should probably be own table cba
    directors = db.Column(db.String(250), nullable=True)
    cast = db.Column(db.String(250), nullable=True)
    genres = db.Column(db.String(250), nullable=True)

    def rel_cover_art_path(self):
        return 'static/cover_arts/' + self.cover_art_name


class ViewingSeat(db.Model):
    __tablename__ = "viewing_seat"
    seat_id = db.Column(db.Integer, db.ForeignKey('seat.id'), unique=True, primary_key=True)
    viewing_id = db.Column(db.Integer, db.ForeignKey('viewing.id'), unique=True, primary_key=True)


class Seat(db.Model):
    __tablename__ = "seat"
    id = db.Column(db.Integer, unique=True, primary_key=True)

    theatre_id = db.Column(db.Integer, db.ForeignKey('theatre.id'), unique=True, primary_key=True)
    # theatre = db.relationship('Theatre', backref='seats', lazy=True)


class Theatre(db.Model):
    __tablename__ = "theatre"
    id = db.Column(db.Integer, unique=True, primary_key=True)

    # seat_id = db.Column(db.Integer, db.ForeignKey('seat.id'), unique=True)
    seats = db.relationship('Seat', backref='theatre', lazy=True)
