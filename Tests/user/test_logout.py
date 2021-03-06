from Tests.user.base_user import UserBaseTestCase

from flask import url_for


class LogoutTestCase(UserBaseTestCase):
    @classmethod
    def setUpClass(cls):
        # Only setup database once since database should not be affected by tests
        cls.db_per_class = True
        super().setUpClass()

    def test_logout_correct(self):
        with self.client:
            self.login_customerA()
            res = self.logout()
            self.assert200(res)
            self.assert_message_flashed('Logout successful', 'success')

    def test_logout_no_csrf(self):
        with self.client:
            self.login_customerA()

            self.client.post(url_for('user.logout'), data={}, follow_redirects=True)

            # No 400 because redirect
            self.assert_message_flashed('Logout failed', 'danger')

    def test_logout_not_logged_in(self):
        with self.client:
            self.logout()

            # No 400 because redirect
            self.assert_message_flashed('Logout failed. No user logged in', 'danger')
