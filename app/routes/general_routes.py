from flask import Blueprint, render_template

general_routes = Blueprint('general_routes', __name__)


@general_routes.route('/')
def home():
    return render_template('home.html')


@general_routes.route('/about')
def about():
    return render_template('about.html')


@general_routes.route('/contact')
def contact():
    return render_template('contact.html')


