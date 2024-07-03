from flask import Blueprint, render_template
from flask_login import login_required

admin_routes = Blueprint('admin_routes', __name__)

@admin_routes.route('/dashboard')
@login_required
def admin_dashboard():
    return render_template('admin/admin_dashboard.html')

@admin_routes.route('/manage-employees')
@login_required
def manage_employees():
    return render_template('admin/manage_employees.html')
