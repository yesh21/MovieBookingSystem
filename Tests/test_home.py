# from Flask_Cinema_Site import db

import unittest
from Tests.base import BaseTestCase


class HomeTestCase(BaseTestCase):
    def setUp(self):
        self.prefix = ''

    def test_home(self):
        with self.client:
            res = self.client.get(f'{self.prefix}/')
            self.assert200(res)
            self.assertIn(b'Home page', res.data)


# Runs Home unit tests
if __name__ == '__main__':
    unittest.main()
