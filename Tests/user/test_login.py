from Tests.user.base_user import UserBaseTestCase


class LoginTestCase(UserBaseTestCase):
    def test_login_loads(self):
        with self.client:
            res = self.client.get('/user/login')
            self.assert200(res)
            self.assertIn(b'Login', res.data)

    def test_login_correct(self):
        with self.client:
            res = self.login_customerA()
            self.assert200(res)
            self.assertIn(b'Login successful', res.data)

    def test_login_correct_redirect(self):
        with self.client:
            params = dict(
                email=self.cA.email,
                password=self.cA.plain_test_password
            )
            res = self.client.post('/user/login?next=%2Fuser%2Fmanage', data=params)
            self.assertRedirects(res, '/user/manage')

    def test_login_redirect_when_logged_in(self):
        with self.client:
            self.login_customerA()
            res = self.client.get('/user/login?next=%2Fuser%2Fmanage')
            self.assertRedirects(res, '/user/manage')

    def test_login_invalid_email(self):
        with self.client:
            res = self.login('not an email', self.cA.plain_test_password)
            self.assert400(res)
            self.assertIn(b'Invalid email', res.data)

    def test_login_not_registered_email(self):
        with self.client:
            res = self.login('not.registered@example.com', self.cA.plain_test_password)
            self.assert400(res)
            self.assertIn(b'Login failed', res.data)

    def test_login_incorrect_password(self):
        with self.client:
            res = self.login(self.cA.email, 'wrong password')
            self.assert400(res)
            self.assertIn(b'Login failed', res.data)
