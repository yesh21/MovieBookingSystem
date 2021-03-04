from flask_testing import TestCase

from Flask_Cinema_Site import app, db
from Flask_Cinema_Site.models import Customer
from Flask_Cinema_Site.forms import SimpleForm

import warnings


class BaseTestCase(TestCase):
    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def add_customers(self):
        self.cA = Customer(
            username='CustomerA',
            first_name='First',
            last_name='Last',
            email='customerA@aaronrosser.xyz'
        )
        self.cA.plain_test_password = 'customerA'
        self.cA.set_password(self.cA.plain_test_password)
        db.session.add(self.cA)

        self.cB = Customer(
            username='CustomerB',
            first_name='First',
            last_name='Last',
            email='customerB@aaronrosser.xyz'
        )
        self.cB.plain_test_password = 'customerB'
        self.cB.set_password(self.cB.plain_test_password)
        db.session.add(self.cB)

        db.session.commit()

    def add_managers(self):
        pass

    def add_movies(self):
        pass

    def setUp(self):
        # Ignore warnings from testing picture uploads
        warnings.simplefilter('ignore', category=ResourceWarning)
        # Ignore warning from escaped . in regex
        warnings.simplefilter('ignore', category=DeprecationWarning)

        # Create in memory database
        db.create_all()

        # Add test data to database
        self.add_customers()
        self.add_managers()
        self.add_movies()

        # Generate csrf token in session
        with self.client:
            self.client.get('/')
        # Get csrf token
        self.csrf_token = SimpleForm().csrf_token.current_token

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def login(self, email, password):
        return self.client.post('/user/login', data=dict(
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
        pass
