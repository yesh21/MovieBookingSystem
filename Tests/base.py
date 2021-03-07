from flask_testing import TestCase

from Flask_Cinema_Site import app, db
from Flask_Cinema_Site.models import Customer
from Flask_Cinema_Site.forms import SimpleForm

from flask import url_for

import warnings


class BaseTestCase(TestCase):
    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    @classmethod
    def setUpClass(cls):
        # Ignore warnings from testing picture uploads
        warnings.simplefilter('ignore', category=ResourceWarning)
        # Ignore warning from escaped . in regex
        warnings.simplefilter('ignore', category=DeprecationWarning)

        # If no tests affect the database then setup per class of tests
        if hasattr(cls, 'db_per_class'):
            cls.setUpDb()

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'db_per_class'):
            db.session.remove()
            db.drop_all()

    def setUp(self):
        # Setup database per test
        if not hasattr(self, 'db_per_class'):
            self.setUpDb()

        # Generate csrf token in session
        with self.client:
            self.client.get('/')
        # Get csrf token
        self.csrf_token = SimpleForm().csrf_token.current_token

    def tearDown(self):
        if not hasattr(self, 'db_per_class'):
            db.session.remove()
            db.drop_all()

    @classmethod
    def add_customers(cls):
        cls.cA = Customer(
            username='CustomerA',
            first_name='First',
            last_name='Last',
            email='customerA@aaronrosser.xyz',
            confirmed=True
        )
        cls.cA.plain_test_password = 'customerA'
        cls.cA.set_password(cls.cA.plain_test_password)
        db.session.add(cls.cA)

        cls.cB = Customer(
            username='CustomerB',
            first_name='First',
            last_name='Last',
            email='customerB@aaronrosser.xyz',
            confirmed=True
        )
        cls.cB.plain_test_password = 'customerB'
        cls.cB.set_password(cls.cB.plain_test_password)
        db.session.add(cls.cB)

        db.session.commit()

    @classmethod
    def add_managers(cls):
        pass

    @classmethod
    def add_movies(cls):
        pass

    @classmethod
    def setUpDb(cls):
        # Create in memory database
        db.create_all()

        # Add test data to database
        cls.add_customers()
        cls.add_managers()
        cls.add_movies()

    def login(self, email, password):
        return self.client.post(url_for('user.login'), data=dict(
            email=email,
            password=password,
            csrf_token=self.csrf_token
        ), follow_redirects=True)

    def login_customerA(self):
        return self.login('customerA@aaronrosser.xyz', 'customerA')

    def login_customerB(self):
        return self.login('customerB@aaronrosser.xyz', 'customerB')

    def login_managerA(self):
        pass

    def login_managerB(self):
        pass

    def logout(self):
        return self.client.post(url_for('user.logout'), data=dict(
            csrf_token=self.csrf_token
        ), follow_redirects=True)
