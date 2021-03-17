from Flask_Cinema_Site import app

from flask_login import current_user
from flask_principal import Permission, RoleNeed, UserNeed, identity_loaded

# Create roles
customer_permission = Permission(RoleNeed('customer'))
manager_permission = Permission(RoleNeed('manager'))
admin_permission = Permission(RoleNeed('admin'))


@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    # Set the identity user object
    identity.user = current_user

    # Add the UserNeed to the identity
    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))

    # Assuming the User model has a list of roles, update the
    # identity with the roles that the user provides
    if hasattr(current_user, 'roles'):
        for role in current_user.roles:
            identity.provides.add(RoleNeed(role.name))
