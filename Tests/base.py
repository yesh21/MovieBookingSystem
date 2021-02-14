from flask_testing import TestCase

from Flask_Cinema_Site import app, db
#from Flask_Cinema_Site.models import *

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

        # Create in memory database
        db.create_all()

        # Add test data to database

        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def login(self):
        pass

    def logout(self):
        pass
