from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
import os
from flask import current_app
from werkzeug.utils import secure_filename
from app.models import Item, Order  # Import your Item model from app.models
from app import db
from app.forms import ItemForm, UpdateOrderStatusForm

employee_routes = Blueprint('employee_routes', __name__)


@employee_routes.route('/dashboard')
@login_required
def employee_dashboard():
    return render_template('employee/employee_dashboard.html')


@employee_routes.route('/add_item', methods=['GET', 'POST'])
@login_required
def add_item():
    form = ItemForm()
    if form.validate_on_submit():
        # Secure and save the image
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            image_path = os.path.join(current_app.root_path, 'static/images', filename)
            form.image.data.save(image_path)
        else:
            filename = None

        # Add item to the database
        new_item = Item(name=form.name.data, description=form.description.data, price=form.price.data, image=filename)
        db.session.add(new_item)
        db.session.commit()

        flash('Item has been added!', 'success')
        return redirect(url_for('employee_routes.employee_dashboard'))

    return render_template('employee/add_item.html', form=form)


def save_image(image):
    import os
    from werkzeug.utils import secure_filename

    if image:
        filename = secure_filename(image.filename)
        image_path = os.path.join('app', 'static', 'images', filename)
        image.save(image_path)
        return filename
    else:
        return None


@employee_routes.route('/manage-orders')
@login_required
def manage_orders():
    orders = Order.query.all()
    form = UpdateOrderStatusForm()
    return render_template('employee/manage_orders.html', orders=orders, form=form)


@employee_routes.route('/update-order-status/<int:order_id>', methods=['POST'])
@login_required
def update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    form = UpdateOrderStatusForm()
    if form.validate_on_submit():
        order.status = form.status.data
        db.session.commit()
        flash('Order status has been updated!', 'success')
    return redirect(url_for('employee_routes.manage_orders'))
