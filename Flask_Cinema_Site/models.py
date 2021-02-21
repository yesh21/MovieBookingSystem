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

    def get_id(self):
        return (self.customerid)
