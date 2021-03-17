# Fix being within folder
import sys
import os
sys.path.insert(0, os.path.dirname(__file__) + '/..')

from Flask_Cinema_Site import db
from Flask_Cinema_Site.models import User, Role

# Add a customer account
customer_role = Role.query.filter_by(name='customer').first()
customer_A = User(
    username='CustomerA',
    first_name='First',
    last_name='Last',
    email='customerA@example.com',
    confirmed=True
)
customer_A.set_password('customerA')
customer_role.users.append(customer_A)

# Add a manager account
manager_role = Role.query.filter_by(name='manager').first()
manager_A = User(
    username='ManagerA',
    first_name='First',
    last_name='Last',
    email='managerA@example.com',
    confirmed=True
)
manager_A.set_password('managerA')
manager_role.users.append(manager_A)

# Add a admin / manager account
admin_role = Role.query.filter_by(name='admin').first()
admin_A = User(
    username='AdminA',
    first_name='First',
    last_name='Last',
    email='adminA@example.com',
    confirmed=True
)
admin_A.set_password('adminA')

admin_role.users.append(admin_A)
manager_role.users.append(admin_A)

db.session.commit()
