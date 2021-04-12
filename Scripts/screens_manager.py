# Fix being within folder
import sys
import os

sys.path.insert(0, os.path.dirname(__file__) + '/..')

from Flask_Cinema_Site import db
from Flask_Cinema_Site.models import Screen, Viewing

from sqlalchemy import func
from datetime import datetime, timedelta


def root_prompt():
    user_choice = input('Cinema screen management: \n'
                        'a) List all screens \n'
                        'b) Add screen \n'
                        'c) List upcoming viewings in given screen \n'
                        'q) Quit\n')

    if user_choice == 'a':
        list_all_screens()
    elif user_choice == 'b':
        add_screen_prompt()
    elif user_choice == 'c':
        list_upcoming_viewings_for_screen()
    elif user_choice == 'q':
        return True
    else:
        print('Invalid input.')

    print('\n')


def list_all_screens():
    print('| {0:^15} | {1:^15} | {2:^28} |'.format('Screen letter', 'Total viewings', 'Total upcoming viewings'))
    print('-' * 68)
    for s in Screen.query.all():
        num_upcoming_viewings = db.session.query(func.count(Viewing.id))\
            .filter(Viewing.screen_id == s.id)\
            .filter(Viewing.time > datetime.utcnow())\
            .first()[0]
        print('| {0:^15} | {1:^15} | {2:^28} |'.format(s.name, len(s.viewings), num_upcoming_viewings))


def add_screen_prompt():
    screen_name = input('Please enter a screen name:\n')

    if Screen.query.filter_by(name=screen_name).first():
        print(f'Screen with name \'{screen_name}\' already exists. Please try again.')
        return

    if len(screen_name) > 5:
        print('Max screen name length is 5. Please try again.')
        return

    if input(f'Confirm adding screen with name \'{screen_name}\'. y / n\n').lower() != 'y':
        print('Add screen aborted')
        return

    # Add screen
    s = Screen(name=screen_name)
    db.session.add(s)
    db.session.commit()

    print(f'Screen with name \'{screen_name}\' successfully added.')


def list_upcoming_viewings_for_screen():
    screen_name = input('Please enter a screen name:\n')

    s = Screen.query.filter_by(name=screen_name).first()
    if not s:
        print(f'Screen with name \'{screen_name}\' not found.')
        return

    viewings = db.session.query(Viewing)\
        .filter(Viewing.screen_id == s.id)\
        .filter(Viewing.time > datetime.utcnow())\
        .order_by(Viewing.time)\
        .all()

    print('| {0:<30} | {1:^15} | {2:^15} | {3:^15} |'.format('Movie name', 'Date', 'Time start', 'Time end'))
    print('-' * 88)
    last_day = None
    for v in viewings:
        # Print day separators
        if last_day is not None and last_day != v.time.date():
            print('-' * 88)
        last_day = v.time.date()

        end_time = v.time + timedelta(minutes=v.movie.duration)
        print('| {0:<30} | {1:^15} | {2:^15} | {3:^15} |'.format(v.movie.name,
                                                                 v.time.strftime('%d/%m/%y'),
                                                                 v.time.strftime('%H:%M'),
                                                                 end_time.strftime('%H:%M')))


while True:
    if root_prompt():
        break
