# Fix being within folder
import sys
import os

sys.path.insert(0, os.path.dirname(__file__) + '/..')

from helper_functions import int_prompt

from Flask_Cinema_Site import db
from Flask_Cinema_Site.models import Role, User


def root_prompt():
    user_choice = input('Cinema account privilege management: \n'
                        'a) List users with manager role \n'
                        'b) List users with admin role \n'
                        'c) Add manager role to user \n'
                        'd) Add manager and admin role to user \n'
                        'q) Quit\n')

    if user_choice == 'a':
        list_manager_users()
    elif user_choice == 'b':
        list_admin_users()
    elif user_choice == 'c':
        add_manager_role_prompt()
    elif user_choice == 'd':
        add_manager_admin_role_prompt()
    elif user_choice == 'q':
        return True
    else:
        print('Invalid input.')

    print('\n')


def list_manager_users():
    manager_role = Role.query.filter_by(name='manager').first()
    print_users(manager_role.users)


def list_admin_users():
    admin_role = Role.query.filter_by(name='admin').first()
    print_users(admin_role.users)


def add_manager_role_prompt():
    u = find_user_by_email()
    if not u:
        return

    print_user(u)

    if input('Confirm adding manager role to selected user. y / n:\n').lower() != 'y':
        return

    manager_role = Role.query.filter_by(name='manager').first()
    manager_role.users.append(u)

    db.session.commit()
    print('Role successfully added.')


def add_manager_admin_role_prompt():
    u = find_user_by_email()
    if not u:
        return

    print_user(u)

    if input('\nConfirm adding manager and admin roles to selected user. y / n:\n').lower() != 'y':
        return

    manager_role = Role.query.filter_by(name='manager').first()
    manager_role.users.append(u)

    admin_role = Role.query.filter_by(name='admin').first()
    admin_role.users.append(u)

    db.session.commit()
    print('Roles successfully added.')


def find_user_by_email() -> User:
    email = input('Please enter the user\'s email address:\n')
    u = User.query.filter_by(email=email).first()
    if not u:
        if input(f'User with email \'{email}\' not found would you like to try again? y / n').lower() == 'y':
            return find_user_by_email()

    return u


def print_user(u: User):
    print('\nSelected user')
    print(f'Name: {u.first_name} {u.last_name}')
    print(f'Email: {u.email}')
    print(f'Username: {u.username}')

    last_login = u.last_login.strftime('%H:%M %d/%m/%Y') if u.last_login is not None else 'never'
    print(f'Last logged in: {last_login}')

    current_roles = [role.name for role in u.roles]
    print('Current roles: ' + ' ,'.join(current_roles))


def print_users(users):
    print('| {0:^5} | {1:<20} | {2:<20} | {3:<20} | {4:<100} |'.format('Id', 'First name', 'Last name',
                                                                       'Last logged in', 'Email'))
    print('-' * 181)
    for u in users:
        last_login = u.last_login.strftime('%H:%M %d/%m/%Y') if u.last_login is not None else 'never'
        print('| {0:^5} | {1:<20} | {2:<20} | {3:<20} | {4:<100} |'.format(u.id, u.first_name, u.last_name, last_login,
                                                                           u.email))


while True:
    if root_prompt():
        break
