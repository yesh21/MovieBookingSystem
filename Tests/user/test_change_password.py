from Tests.user.base_user import UserBaseTestCase

from flask import url_for


class ChangePasswordTestCase(UserBaseTestCase):
    # Success
    def test_user_change_password_correct_same(self):
        with self.client:
            self.login_customerA()

            params = dict(
                current_password=self.customer_A.plain_test_password,
                password=self.customer_A.plain_test_password,
                password_confirm=self.customer_A.plain_test_password,
                csrf_token=self.csrf_token
            )
            res = self.client.post(url_for('user.change_password'), data=params)
            self.assert200(res)

            # Ensure password was changed (new salt)
            self.assertTrue(self.customer_A.check_password(self.customer_A.plain_test_password))

    # Fail
    def test_user_change_password_correct(self):
        with self.client:
            self.login_customerA()
            new_password = 'new password 123'

            params = dict(
                current_password=self.customer_A.plain_test_password,
                password=new_password,
                password_confirm=new_password,
                csrf_token=self.csrf_token
            )
            res = self.client.post(url_for('user.change_password'), data=params)
            self.assert200(res)

            # Ensure password was changed
            self.assertTrue(self.customer_A.check_password(new_password))

    def test_user_change_password_incorrect_password(self):
        with self.client:
            self.login_customerA()
            new_password = 'new password 123'

            params = dict(
                current_password='not the current password',
                password=new_password,
                password_confirm=new_password,
                csrf_token=self.csrf_token
            )
            res = self.client.post(url_for('user.change_password'), data=params)
            self.assert400(res)

            # Ensure password was not changed
            self.assertTrue(self.customer_A.check_password(self.customer_A.plain_test_password))

    def test_user_change_password_invalid_form(self):
        with self.client:
            self.login_customerA()

            params = dict(
                current_password=self.customer_A.plain_test_password,
                password='a new password',
                password_confirm='not the same new password',
                csrf_token=self.csrf_token
            )
            res = self.client.post(url_for('user.change_password'), data=params)
            self.assert400(res)

            # Ensure password was not changed
            self.assertTrue(self.customer_A.check_password(self.customer_A.plain_test_password))

    def test_user_change_password_no_csrf(self):
        with self.client:
            self.login_customerA()
            new_password = 'new password 123'

            params = dict(
                current_password=self.customer_A.plain_test_password,
                password=new_password,
                password_confirm=new_password
            )
            res = self.client.post(url_for('user.change_password'), data=params)
            self.assert400(res)

            # Ensure password was changed
            self.assertTrue(self.customer_A.check_password(self.customer_A.plain_test_password))
