from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from app import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    orders = db.relationship('Order', backref='customer', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(120), nullable=True)

    def __repr__(self):
        return f"Item('{self.name}', '{self.price}')"


class BuyForm(FlaskForm):
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Place Order')


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    items = db.Column(db.Text, nullable=False)  # This can be a JSON string
    status = db.Column(db.String(20), default='Pending', nullable=False)
    address = db.Column(db.String(200))  # Add this line for address

    def __repr__(self):
        return f"Order('{self.id}', '{self.user_id}', '{self.items}', '{self.status}', '{self.address}')"

