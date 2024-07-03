from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app import db


auth_routes = Blueprint('auth_routes', __name__)


@auth_routes.route("/login", methods=['GET', 'POST'])
def auth_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Find the user by email
        user = User.query.filter_by(email=email).first()

        # Check if user exists and verify the password
        if user and password:
            login_user(user)
            flash('Logged in successfully.', 'success')
            user_role = user.role
            if user_role == "customer":
                return redirect(url_for('customer_routes.customer_dashboard'))
            elif user_role == "employee":
                return redirect(url_for('employee_routes.employee_dashboard'))
            elif user_role == "admin":
                return redirect(url_for('admin_routes.admin_dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('login.html')


@auth_routes.route("/logout")
@login_required
def auth_logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('general_routes.home'))
