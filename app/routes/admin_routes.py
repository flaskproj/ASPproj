from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app import db
from app.forms import EditEmployeeForm
from app.models import User

admin_routes = Blueprint('admin_routes', __name__)

@admin_routes.route('/dashboard')
@login_required
def admin_dashboard():
    return render_template('admin/admin_dashboard.html')

@admin_routes.route('/manage-employees', methods=['GET', 'POST'])
@login_required
def manage_employees():
    employees = User.query.filter_by(role='employee').all()
    return render_template('admin/manage_employees.html', employees=employees)

@admin_routes.route('/edit-employee/<int:employee_id>', methods=['GET', 'POST'])
@login_required
def edit_employee(employee_id):
    employee = User.query.get_or_404(employee_id)
    form = EditEmployeeForm()

    if form.validate_on_submit():
        employee.username = form.username.data
        employee.email = form.email.data
        db.session.commit()
        flash('Employee information updated successfully!', 'success')
        return redirect(url_for('admin_routes.manage_employees'))

    elif request.method == 'GET':
        form.username.data = employee.username
        form.email.data = employee.email

    return render_template('admin/edit_employee.html', form=form, employee=employee)

@admin_routes.route('/delete-employee/<int:employee_id>', methods=['POST'])
@login_required
def delete_employee(employee_id):
    employee = User.query.get_or_404(employee_id)
    db.session.delete(employee)
    db.session.commit()
    flash('Employee deleted successfully!', 'success')
    return redirect(url_for('admin_routes.manage_employees'))
