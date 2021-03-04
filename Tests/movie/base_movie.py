# from Flask_Cinema_Site import db

from Tests.base import BaseTestCase


class MovieBaseTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.prefix = '/movie'
