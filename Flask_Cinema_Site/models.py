from Flask_Cinema_Site import db, app, bcrypt

from flask import Markup
from flask_login import UserMixin

from datetime import datetime
from time import time
from math import floor
import jwt


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)

    users = db.relationship('User', secondary='user_role', back_populates='roles', sync_backref=False)


class UserRole(db.Model):
    __tablename__ = 'user_role'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), primary_key=True)


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)

    transactions = db.relationship('Transaction', backref='user', lazy=True)

    # Readonly list
    roles = db.relationship('Role', secondary='user_role', back_populates='users', viewonly=True)

    # Data fields
    email = db.Column(db.String(320), nullable=False, unique=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)

    created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    last_login = db.Column(db.DateTime, nullable=True)

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
        return User.query.get(id)

    def get_email_confirm_token(self, expires_in=86400):
        return jwt.encode(
            {'email_confirm': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_email_confirm_token(token):
        try:
            user_id = jwt.decode(token, app.config['SECRET_KEY'],
                                 algorithms=['HS256'])['email_confirm']
        except jwt.ExpiredSignatureError:
            return
        except jwt.DecodeError:
            return
        except jwt.InvalidTokenError:
            return
        return User.query.get(user_id)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')


class Transaction(db.Model):
    __tablename__ = "transaction"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    seats = db.relationship('Seat', backref='transaction', lazy=True)

    # Readonly list
    viewings = db.relationship('Viewing', secondary='seat', back_populates='transactions', viewonly=True,
                               sync_backref=False)

    datetime = db.Column(db.DateTime, nullable=False, default=datetime.now())


class Viewing(db.Model):
    __tablename__ = "viewing"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    theatre_id = db.Column(db.Integer, db.ForeignKey('theatre.id'))

    seats = db.relationship('Seat', backref='viewing', lazy=True)

    # Readonly list
    transactions = db.relationship('Transaction', secondary='seat', back_populates='viewings', viewonly=True,
                                   sync_backref=False)

    # TODO Rename to datetime?
    time = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Float, nullable=False)


class Movie(db.Model):
    __tablename__ = "movie"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    viewings = db.relationship('Viewing', backref='movie', lazy=True)

    # Data fields
    # TODO Fix string lengths
    name = db.Column(db.String(100), nullable=False)
    overview = db.Column(db.String(500), nullable=False)
    released = db.Column(db.Date, nullable=False)

    duration = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    hidden = db.Column(db.Boolean, nullable=False)

    cover_art_name = db.Column(db.String(35), nullable=False)

    # Should probably be own table cba
    directors = db.Column(db.String(250), nullable=True)
    cast = db.Column(db.String(250), nullable=True)
    genres = db.Column(db.String(250), nullable=True)

    def rel_cover_art_path(self):
        return 'cover_arts/' + self.cover_art_name

    def get_star_rating_html(self):
        # Full stars
        stars = '<i class="bi bi-star-fill mr-1"></i>' * floor(self.rating)
        # Half star
        if self.rating != floor(self.rating):
            stars += '<i class="bi bi-star-half mr-1"></i>'
        # Empty stars
        stars += '<i class="bi bi-star mr-1"></i>' * floor(5 - self.rating)
        return Markup(stars)


class Seat(db.Model):
    __tablename__ = "seat"
    id = db.Column(db.Integer, primary_key=True)
    viewing_id = db.Column(db.Integer, db.ForeignKey('viewing.id'), nullable=False)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'), nullable=True)

    # Needs to be unique to viewing only
    seat_number = db.Column(db.String(10), nullable=False)


class Theatre(db.Model):
    __tablename__ = "theatre"
    id = db.Column(db.Integer, unique=True, primary_key=True)

    viewings = db.relationship('Viewing', backref='viewing', lazy=True)
