from Flask_Cinema_Site import db

import unittest
from Tests.base import BaseTestCase


class UserTestCase(BaseTestCase):
    def setUp(self):
        self.prefix = '/user'

    def test_user(self):
        with self.client:
            res = self.client.get(f'{self.prefix}/')
            self.assert200(res)
            self.assertIn(b'User page', res.data)


# Runs user unit tests
if __name__ == '__main__':
    unittest.main()