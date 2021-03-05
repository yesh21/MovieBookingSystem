from Tests.user.base_user import UserBaseTestCase

from Flask_Cinema_Site.models import Customer

from flask import url_for


class RegisterTestCase(UserBaseTestCase):
    def test_register_loads(self):
        with self.client:
            res = self.client.get(url_for('user.signup'))
            self.assert200(res)
            self.assertIn(b'Register', res.data)

    def test_register_redirect_when_logged_in(self):
        with self.client:
            self.login_customerA()
            res = self.client.post(url_for('user.signup'))
            # Default for get_redirect_url
            self.assertRedirects(res, '/')

    def test_register_correct(self):
        with self.client:
            params = dict(
                first_name='first',
                last_name='last',
                username='username',
                email='email@example.com',
                password='password',
                password_confirm='password',
                consent=True,
                csrf_token=self.csrf_token
            )
            res = self.client.post(url_for('user.signup'), data=params, follow_redirects=True)

            self.assert200(res)
            self.assert_message_flashed('New user \'username\' was successfully created', 'success')

            u = Customer.query.filter_by(
                email='email@example.com'
            ).first()
            self.assertEqual(u.first_name, 'first')
            self.assertEqual(u.last_name, 'last')
            self.assertEqual(u.username, 'username')
            self.assertIsNotNone(u.password_hash)

    def test_register_incorrect_dup_details(self):
        with self.client:
            params = dict(
                first_name='first',
                last_name='last',
                username=self.cA.username,
                email=self.cA.email,
                password='password',
                password_confirm='password',
                consent=True,
                csrf_token=self.csrf_token
            )
            res = self.client.post(url_for('user.signup'), data=params, follow_redirects=True)

            self.assert400(res)
            self.assertIn(f'Username \'{self.cA.username}\' already exists'.encode(), res.data)
            self.assertIn(f'Email \'{self.cA.email}\' already exists'.encode(), res.data)

            users = Customer.query.filter_by(
                email=self.cA.email
            ).all()
            self.assertTrue(len(users) == 1)

    def test_register_incorrect_invalid_form(self):
        with self.client:
            params = dict(
                first_name='f',
                last_name='l',
                username='very long username greater than 25 characters',
                email='not an email',
                password='different passwords',
                password_confirm='different passwords 123',
                consent=True,
                csrf_token=self.csrf_token
            )
            res = self.client.post(url_for('user.signup'), data=params, follow_redirects=True)
            self.assert400(res)
            self.assertIn(f'Field must be between 3 and {Customer.first_name.type.length}'
                          f' characters long.'.encode(), res.data)
            self.assertIn(b'Invalid email address', res.data)
            self.assertIn(b'Passwords must match', res.data)

            u = Customer.query.filter_by(
                email='not an email'
            ).first()
            self.assertIsNone(u)

    def test_register_no_csrf(self):
        with self.client:
            params = dict(
                first_name='first',
                last_name='last',
                username='username',
                email='email@example.com',
                password='password',
                password_confirm='password',
                consent=True
            )
            res = self.client.post(url_for('user.signup'), data=params, follow_redirects=True)
            self.assert400(res)

            u = Customer.query.filter_by(
                email='not an email'
            ).first()
            self.assertIsNone(u)
