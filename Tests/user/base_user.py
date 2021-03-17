from Tests.base import BaseTestCase

from Flask_Cinema_Site.models import User


class UserBaseTestCase(BaseTestCase):
    def assert_details_equal(self, u: User, params):
        self.assertEqual(params['first_name'], u.first_name)
        self.assertEqual(params['last_name'], u.last_name)
        self.assertEqual(params['username'], u.username)
        self.assertEqual(params['email'], u.email)

    def assert_details_not_equal(self, u: User, params):
        self.assertNotEqual(params['first_name'], u.first_name)
        self.assertNotEqual(params['last_name'], u.last_name)
        self.assertNotEqual(params['username'], u.username)
        self.assertNotEqual(params['email'], u.email)

    def user_to_params(self, u):
        return dict(
            first_name=u.first_name,
            last_name=u.last_name,
            username=u.username,
            email=u.email,
            csrf_token=self.csrf_token
        )
