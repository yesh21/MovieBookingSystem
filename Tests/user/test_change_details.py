from Tests.user.base_user import UserBaseTestCase

from Flask_Cinema_Site import db

from flask import url_for


class ChangeDetailsTestCase(UserBaseTestCase):
    # Success
    def test_change_user_details_correct_same(self):
        with self.client:
            self.login_customerA()

            params = self.user_to_params(self.customer_A)
            res = self.client.post(url_for('user.update_user_details'), data=params)

            self.assert200(res)
            self.assert_details_equal(self.customer_A, params)
            self.assertEqual(self.customer_A.confirmed, True)

    def test_change_user_details_correct_same_not_confirmed(self):
        with self.client:
            self.customer_A.confirmed = False
            db.session.commit()
            self.login_customerA()

            params = self.user_to_params(self.customer_A)
            res = self.client.post(url_for('user.update_user_details'), data=params)

            self.assert200(res)
            self.assert_details_equal(self.customer_A, params)
            self.assertEqual(self.customer_A.confirmed, False)

    def test_change_user_details_correct_changed(self):
        with self.client:
            self.login_customerA()

            params = dict(
                first_name='new first name',
                last_name='new last name',
                username='new username',
                email='new.email@example.com',
                csrf_token=self.csrf_token
            )
            res = self.client.post(url_for('user.update_user_details'), data=params)

            self.assert200(res)
            self.assert_details_equal(self.customer_A, params)
            self.assertEqual(self.customer_A.confirmed, False)

    # Fail
    def test_change_user_details_invalid(self):
        with self.client:
            self.login_customerA()

            params = dict(
                first_name='f',
                last_name='f',
                username='new realllllllly long username',
                email='not an email',
                csrf_token=self.csrf_token
            )
            res = self.client.post(url_for('user.update_user_details'), data=params)

            self.assert400(res)
            self.assertIn(b'Field must be between 3 and 20 characters long.', res.data)
            self.assertIn(b'Invalid email address.', res.data)

            self.assert_details_not_equal(self.customer_A, params)
            self.assertEqual(self.customer_A.confirmed, True)

    def test_change_user_details_duplicate(self):
        with self.client:
            self.login_customerA()

            params = self.user_to_params(self.customer_B)
            res = self.client.post(url_for('user.update_user_details'), data=params)

            self.assert400(res)
            self.assert_details_not_equal(self.customer_A, params)
            self.assertEqual(self.customer_A.confirmed, True)

            self.assertIn(b'Username already registered to an account.', res.data)
            self.assertIn(b'Email already registered to an account.', res.data)

    def test_change_user_details_no_csrf(self):
        with self.client:
            self.login_customerA()

            params = dict(
                first_name='new first name',
                last_name='new last name',
                username='new username',
                email='new.email@example.com'
            )
            res = self.client.post(url_for('user.update_user_details'), data=params)

            self.assert400(res)
            self.assert_details_not_equal(self.customer_A, params)
            self.assertEqual(self.customer_A.confirmed, True)
