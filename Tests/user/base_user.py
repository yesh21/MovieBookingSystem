# from Flask_Cinema_Site import db

from Tests.base import BaseTestCase


class UserBaseTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.prefix = '/user'
