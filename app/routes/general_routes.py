from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, logout_user

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


@general_routes.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('general_routes.home'))
