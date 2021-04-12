# Fix being within folder
import sys
import os

sys.path.insert(0, os.path.dirname(__file__) + '/..')

from helper_functions import int_prompt, datetime_prompt

from Flask_Cinema_Site import db
from Flask_Cinema_Site.models import Movie, Viewing, Screen

from sqlalchemy import func
from datetime import datetime, timedelta, date


def root_prompt():
    user_choice = input('Cinema viewings management: \n'
                        'a) Add viewing to movie \n'
                        'b) List upcoming viewings for given movie\n'
                        'q) Quit\n')

    if user_choice == 'a':
        add_viewing_prompt()
    elif user_choice == 'b':
        list_upcoming_viewings_for_movie()
    elif user_choice == 'q':
        return True
    else:
        print('Invalid input.')

    print('\n')


def add_viewing_prompt():
    m = get_movie_prompt()
    if not m:
        return

    if input(f'You selected \'{m.name}\'. Continue y / n ?\n').lower() != 'y':
        return

    list_all_screens()
    screen_letter = input('Please enter a screen name:\n')

    s = Screen.query.filter_by(name=screen_letter).first()
    if not s:
        print(f'Screen with letter \'{screen_letter}\' not found.')
        return

    viewing_date = datetime_prompt('Please enter the new viewings date in the format dd/mm/yyyy, eg 01/01/2021\n',
                                   '%d/%m/%Y').date()
    list_viewings_for_screen_on_date(s, viewing_date)

    viewing_time = datetime_prompt('Please enter the new viewings start time in the format HH:MM, eg 21:02\n' +
                                   f'Note: {m.name}\'s duration is {m.duration} minutes.\n', '%H:%M').time()

    if input(f'Add a viewing for \'{m.name}\' on screen \'{s.name}\' at \'{viewing_time.strftime("%H:%M")}\' on '
             f'\'{viewing_date.strftime("%d/%m/%Y")}\'. Confirm y / n:\n').lower() != 'y':
        return

    # Add screen
    v = Viewing(movie_id=m.id, screen_id=s.id, time=datetime.combine(viewing_date, viewing_time))
    v.init_seats()
    db.session.add(v)
    db.session.commit()

    print('Viewing added successfully')


def list_upcoming_viewings_for_movie():
    m = get_movie_prompt()
    if not m:
        return

    viewings = db.session.query(Viewing) \
        .filter(Viewing.movie_id == m.id) \
        .filter(Viewing.time > datetime.utcnow()) \
        .order_by(Viewing.time) \
        .all()

    print('| {0:^77} |'.format('Upcoming viewings for ' + m.name))
    print('-' * 81)
    print('| {0:^5} | {1:^15} | {2:^15} | {3:^15} | {4:^15} |'.format('Id', 'Screen name', 'Date', 'Time start',
                                                                      'Time end'))
    print('-' * 81)
    last_day = None
    for v in viewings:
        # Print day separators
        if last_day is not None and last_day != v.time.date():
            print('-' * 81)
        last_day = v.time.date()

        end_time = v.time + timedelta(minutes=v.movie.duration)
        print('| {0:^5} | {1:^15} | {2:^15} | {3:^15} | {4:^15} |'.format(v.id, v.screen.name,
                                                                          v.time.strftime('%d/%m/%y'),
                                                                          v.time.strftime('%H:%M'),
                                                                          end_time.strftime('%H:%M')))


def list_all_movies():
    """
    Lists all movies id, name, year and number of upcoming viewings
    """
    print('| {0:^107} |'.format('Movies'))
    print('-' * 111)
    print('| {0:^5} | {1:<60} | {2:^8} | {3:^25} |'.format('Id', 'Name', 'Year', 'Number upcoming viewings'))
    print('-' * 111)
    for m in Movie.query.all():
        num_upcoming_viewings = db.session.query(func.count(Viewing.id)) \
            .filter(Viewing.movie_id == m.id) \
            .filter(Viewing.time > datetime.utcnow()) \
            .first()[0]
        print('| {0:^5} | {1:<60} | {2:^8} | {3:^25} |'.format(m.id, m.name, m.released.strftime('%Y'),
                                                               num_upcoming_viewings))


def get_movie_prompt() -> Movie:
    list_all_movies()
    movie_id = int_prompt('Please enter a movie id:\n')

    m = Movie.query.get(movie_id)
    if not m:
        print(f'Movie with id \'{movie_id}\' not found.')

    return m


def list_all_screens():
    """
    Lists all screen names along with number of upcoming viewings
    """
    print('| {0:^15} | {1:^28} |'.format('Screen name', 'Total upcoming viewings'))
    print('-' * 68)
    for s in Screen.query.all():
        num_upcoming_viewings = db.session.query(func.count(Viewing.id)) \
            .filter(Viewing.screen_id == s.id) \
            .filter(Viewing.time > datetime.utcnow()) \
            .first()[0]
        print('| {0:^15} | {1:^28} |'.format(s.name, num_upcoming_viewings))


def list_viewings_for_screen_on_date(s: Screen, d: date):
    viewings = db.session.query(Viewing) \
        .filter(Viewing.screen_id == s.id) \
        .filter(func.date(Viewing.time) == d) \
        .all()

    print('| {0:^66} |'.format('Viewings on date: ' + d.strftime('%d/%m/%Y')))
    print('-' * 70)
    print('| {0:<30} | {1:^15} | {2:^15} |'.format('Movie name', 'Time start', 'Time end'))
    print('-' * 70)
    last_day = None
    for v in viewings:
        # Print day separators
        if last_day is not None and last_day != v.time.date():
            print('-' * 88)
        last_day = v.time.date()

        end_time = v.time + timedelta(minutes=v.movie.duration)
        print('| {0:<30} | {1:^15} | {2:^15} |'.format(v.movie.name, v.time.strftime('%H:%M'),
                                                       end_time.strftime('%H:%M')))


while True:
    if root_prompt():
        break
