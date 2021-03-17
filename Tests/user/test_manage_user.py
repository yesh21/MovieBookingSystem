from Tests.user.base_user import UserBaseTestCase

from flask import url_for


class ManageUserTestCase(UserBaseTestCase):
    # Success
    def test_manage_user_loads(self):
        with self.client:
            self.login_customerA()
            res = self.client.get(url_for('user.manage'))

            self.assert200(res)
            self.assertIn(b'Update Details', res.data)
            self.assertIn(b'Change Password', res.data)

            # Ensure shown details are correct
            self.assertIn(self.customer_A.first_name.encode(), res.data)
            self.assertIn(self.customer_A.last_name.encode(), res.data)
            self.assertIn(self.customer_A.username.encode(), res.data)
            self.assertIn(self.customer_A.email.encode(), res.data)

    # Fail
    def test_manage_user_unauthenticated(self):
        with self.client:
            res = self.client.get(url_for('user.manage'))
            self.assertRedirects(res, url_for('user.login', next=url_for('user.manage')))
