from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
import logging
logging.basicConfig(level=logging.INFO)  # Set log level to INFO or DEBUG
from app.forms import ContactForm
from app.models import User, Item, Order, BuyForm
from app import db, mail
from flask_mail import Message

customer_routes = Blueprint('customer_routes', __name__)


@customer_routes.route('/customer/dashboard')
@login_required
def customer_dashboard():
    return render_template('customer/customer_dashboard.html')


@customer_routes.route('/customer/register', methods=['GET', 'POST'])
def customer_register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Check if the username or email already exists
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Username or Email already exists. Please choose another one.', 'danger')
            return redirect(url_for('customer_routes.customer_register'))

        # Create a new user
        new_user = User(username=username, email=email, password=password, role='customer')

        # Add the user to the database
        db.session.add(new_user)
        db.session.commit()

        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('auth_routes.auth_login'))

    return render_template('customer/customer_register.html')


@customer_routes.route('/customer/contact', methods=['GET', 'POST'])
@login_required
def customer_contact():
    form = ContactForm()

    if form.validate_on_submit():
        message_content = form.message.data
        sender_username = current_user.username

        # Construct and send the email
        msg = Message(subject=f"Message from {sender_username}",
                      sender="noreply.norereply@gmail.com",
                      recipients=["noreply.norereply@gmail.com"],
                      body=f"Sender: {sender_username}\n\nMessage:\n{message_content}")

        try:
            mail.send(msg)
            logging.info('Email sent successfully.')  # Logging success
            flash('Your message has been sent!', 'success')
        except Exception as e:
            logging.error(f'Error sending email: {str(e)}')  # Logging error
            flash(f'An error occurred while sending your message: {str(e)}', 'error')

        return redirect(url_for('customer_routes.customer_contact'))

    return render_template('customer/customer_contact.html', form=form)


def send_email(subject, sender, recipients, body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = body
    mail.send(msg)


@customer_routes.route('/customer-orders')
@login_required
def customer_orders():
    orders = Order.query.filter_by(user_id=current_user.id).all()
    return render_template('customer-orders.html', orders=orders)


@customer_routes.route('/mobiles')
@login_required
def mobiles():
    items = Item.query.all()
    return render_template('mobiles.html', items=items)


@customer_routes.route('/buy/<int:item_id>', methods=['GET', 'POST'])
@login_required
def buy_item(item_id):
    item = Item.query.get_or_404(item_id)
    form = BuyForm()
    if form.validate_on_submit():
        address = form.address.data  # Access the address from the form
        order = Order(user_id=current_user.id, items=item.name, status='Pending', address=address)
        db.session.add(order)
        db.session.commit()
        flash('Your order has been placed!', 'success')
        return redirect(url_for('customer_routes.customer_orders'))  # Redirect to orders page after placing order
    return render_template('buy.html', form=form, item=item)


@customer_routes.route('/customer/logout')
@login_required
def customer_logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('general_routes.home'))


# testing:

@customer_routes.route('/recqres-data')
def recqres_data():
    return render_template('recqres-data.html')


@customer_routes.route('/items')
def get_items():
    return render_template('items.html')


@customer_routes.route('/items/json')
def items_json():
    items = Item.query.all()
    item_list = [{'name': item.name, 'description': item.description, 'price': item.price} for item in items]
    return jsonify(items=item_list)


@customer_routes.route('/items/json')
def get_items_json():
    # Fetch items from the database or any other source
    items = Item.query.all()  # Example query to fetch all items

    # Transform items into a JSON serializable format
    items_list = []
    for item in items:
        items_list.append({
            'id': item.id,
            'name': item.name,
            'description': item.description,
            'price': item.price,
            'image': item.image
        })

    return jsonify(items_list)
