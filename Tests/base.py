from flask_testing import TestCase

from Flask_Cinema_Site import app, db
from Flask_Cinema_Site.models import User, Movie, Viewing, Role, Screen
from Flask_Cinema_Site.forms import SimpleForm

from flask import url_for, current_app

from io import BytesIO
from datetime import datetime, date, timedelta
from shutil import copy2
import os
import warnings


class BaseTestCase(TestCase):
    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        # Ignore warnings from testing picture uploads
        warnings.simplefilter('ignore', category=ResourceWarning)
        # Ignore warning from escaped . in regex
        warnings.simplefilter('ignore', category=DeprecationWarning)

        # Setup database per test
        self.setUpDb()

        # Generate csrf token in session
        with self.client:
            self.client.get(url_for('user.login'))
        # Get csrf token
        self.csrf_token = SimpleForm().csrf_token.current_token

    def tearDown(self):
        if not hasattr(self, 'db_per_class'):
            db.session.remove()
            db.drop_all()

    def setUpDb(self):
        # Create in memory database
        db.create_all()

        # Add test data to database
        self.add_roles()
        self.add_customers()
        self.add_managers()
        self.add_movies()
        self.add_viewings()

    def add_roles(self):
        db.session.add(Role(name='customer'))
        db.session.add(Role(name='manager'))
        db.session.add(Role(name='admin'))
        db.session.commit()

    def add_customers(self):
        customer_role = Role.query.filter_by(name='customer').first()

        self.customer_A = User(
            username='CustomerA',
            first_name='FirstA',
            last_name='LastA',
            email='customerA@example.com',
            confirmed=True
        )
        self.customer_A.plain_test_password = 'customerA'
        self.customer_A.set_password(self.customer_A.plain_test_password)
        customer_role.users.append(self.customer_A)

        self.customer_B = User(
            username='CustomerB',
            first_name='FirstB',
            last_name='LastB',
            email='customerB@example.com',
            confirmed=True
        )
        self.customer_B.plain_test_password = 'customerB'
        self.customer_B.set_password(self.customer_B.plain_test_password)
        customer_role.users.append(self.customer_B)

        db.session.commit()

    def add_managers(self):
        manager_role = Role.query.filter_by(name='manager').first()

        self.manager_A = User(
            username='ManagerA',
            first_name='FirstA',
            last_name='LastA',
            email='managerA@example.com',
            confirmed=True
        )
        self.manager_A.plain_test_password = 'managerA'
        self.manager_A.set_password(self.manager_A.plain_test_password)
        manager_role.users.append(self.manager_A)

        self.manager_B = User(
            username='ManagerB',
            first_name='FirstB',
            last_name='LastB',
            email='managerB@example.com',
            confirmed=True
        )
        self.manager_B.plain_test_password = 'managerB'
        self.manager_B.set_password(self.manager_B.plain_test_password)
        manager_role.users.append(self.manager_B)

        db.session.commit()

    def add_movies(self):
        self.movie_A = Movie(
            name='Black Widow',
            overview='In Marvel Studios’ action-packed spy thriller “Black Widow,” '
                     'Natasha Romanoff aka Black Widow confronts the darker parts of '
                     'her ledger when a dangerous conspiracy with ties to her past '
                     'arises. Pursued by a force that will stop at nothing to bring '
                     'her down, Natasha must deal with her history as a spy and the '
                     'broken relationships left in her wake long before she became an Avenger.',
            released=date(2021, 5, 7),
            cover_art_name='black_widow.jpg',
            directors='Cate Shortland',
            cast='Rachel Weisz, David Harbour, O-T Fagbenle, Ray Winstone, Florence '
                 'Pugh, Scarlett Johansson',
            genres='sci-fi',
            duration=123,
            rating=4.2,
            hidden=False
        )
        db.session.add(self.movie_A)

        self.movie_B = Movie(
            name='Ghostbusters: Afterlife',
            overview='From director Jason Reitman and producer Ivan Reitman, comes the next chapter '
                     'in the original Ghostbusters universe. In Ghostbusters: Afterlife, when a single '
                     'mom and her two kids arrive in a small town, they begin to discover their connection '
                     'to the original ghostbusters and the secret legacy their grandfather left behind. '
                     'The film is written by Jason Reitman & Gil Kenan.',
            released=date(2021, 6, 11),
            cover_art_name='ghostbusters.jpg',
            directors='Jason Reitman',
            cast='Finn Wolfhard, Bill Murray, Dan Aykroyd, Sigourney Weaver, Ernie Hudson, Paul Rudd, '
                 'McKenna Grace, Carrie Coon, Bokeem Woodbine, Annie Potts',
            genres='sci-fi',
            duration=125,
            rating=3.5,
            hidden=False
        )
        db.session.add(self.movie_B)

        db.session.commit()

    def add_viewings(self):
        # Add some times for each movie
        viewing_times = [
            datetime.today().replace(hour=10, minute=0, second=0, microsecond=0),
            datetime.today().replace(hour=14, minute=15, second=0, microsecond=0),
            datetime.today().replace(hour=17, minute=30, second=0, microsecond=0)
        ]

        # For simplicity give each movie its own screen
        screen_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                          'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

        for m, screen_letter in zip(Movie.query.all(), screen_letters):
            screen = Screen(name=screen_letter)
            db.session.add(screen)
            db.session.commit()

            # Add viewings for the next 7 days
            for day_num in range(7):
                for viewing_time in viewing_times:
                    m.viewings.append(Viewing(
                        time=viewing_time + timedelta(days=day_num, minutes=20 * day_num),
                        screen_id=screen.id
                    ))

        db.session.commit()

    def copy_resources(self):
        tests_res_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Resources')
        cover_art_path = os.path.join(current_app.root_path, 'movie', 'static', 'cover_arts')

        copy2(os.path.join(tests_res_path, 'black_widow.jpg'), os.path.join(cover_art_path, 'black_widow.jpg'))
        copy2(os.path.join(tests_res_path, 'ghostbusters.jpg'), os.path.join(cover_art_path, 'ghostbusters.jpg'))

    def login(self, email, password):
        return self.client.post(url_for('user.login'), data=dict(
            email=email,
            password=password,
            csrf_token=self.csrf_token
        ), follow_redirects=True)

    def login_customerA(self):
        return self.login(self.customer_A.email, self.customer_A.plain_test_password)

    def login_customerB(self):
        return self.login(self.customer_B.email, self.customer_B.plain_test_password)

    def login_managerA(self):
        return self.login(self.manager_A.email, self.manager_A.plain_test_password)

    def login_managerB(self):
        return self.login(self.manager_B.email, self.manager_B.plain_test_password)

    def logout(self):
        return self.client.post(url_for('user.logout'), data=dict(
            csrf_token=self.csrf_token
        ), follow_redirects=True)

    def get_file_parameter(self, file_name='ghostbusters.jpg'):
        tests_dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(tests_dir_path, 'Resources', file_name)
        with open(file_path, 'rb') as pic:
            return BytesIO(pic.read()), file_name

    def assert_json_response(self, res, msg, status):
        self.assertStatus(res, status)
        self.assertEqual(res.json['code'], status)
        self.assertEqual(res.json['msg'], msg)
