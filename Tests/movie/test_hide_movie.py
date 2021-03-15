from Tests.movie.base_movie import MovieBaseTestCase

from Flask_Cinema_Site import db

from flask import url_for
from flask_api import status


class HideMovieTestCase(MovieBaseTestCase):
    def send_hide_request(self, hidden):
        self.mA.hidden = hidden
        db.session.commit()

        params = dict(
            id=self.mA.id,
            csrf_token=self.csrf_token
        )
        return self.client.post(url_for('movie.hide'), data=params, follow_redirects=True)

    # Success
    def test_hide_hidden_movie_manager(self):
        with self.client:
            self.login_managerA()
            res = self.send_hide_request(True)

            self.assert_json_response(res, f'Movie with id \'{self.mA.id}\' successfully hidden', status.HTTP_200_OK)
            self.assertEqual(self.mA.hidden, True)

    def test_hide_visible_movie_manager(self):
        with self.client:
            self.login_managerA()
            res = self.send_hide_request(False)

            self.assert_json_response(res, f'Movie with id \'{self.mA.id}\' successfully hidden', status.HTTP_200_OK)
            self.assertEqual(self.mA.hidden, True)

    # Fail
    def test_hide_movie_non_existent(self):
        with self.client:
            self.login_managerA()

            params = dict(
                id=999,
                csrf_token=self.csrf_token
            )
            res = self.client.post(url_for('movie.hide'), data=params, follow_redirects=True)

            self.assert_json_response(res, 'Movie with id \'999\' not found', status.HTTP_400_BAD_REQUEST)

    def test_hide_visible_movie_no_id(self):
        with self.client:
            self.login_managerA()
            self.mA.hidden = False
            db.session.commit()

            params = dict(
                csrf_token=self.csrf_token
            )
            res = self.client.post(url_for('movie.hide'), data=params, follow_redirects=True)

            self.assert_json_response(res, 'Error hide movie failed', status.HTTP_400_BAD_REQUEST)
            self.assertEqual(self.mA.hidden, False)

    def test_hide_visible_movie_no_csrf(self):
        with self.client:
            self.login_managerA()
            self.mA.hidden = False
            db.session.commit()

            params = dict(
                id=self.mA.id
            )
            res = self.client.post(url_for('movie.hide'), data=params, follow_redirects=True)

            self.assert_json_response(res, 'Error hide movie failed', status.HTTP_400_BAD_REQUEST)
            self.assertEqual(self.mA.hidden, False)

    def test_hide_visible_movie_customer(self):
        with self.client:
            self.login_managerA()
            res = self.send_hide_request(False)

            # TODO

    def test_hide_visible_movie_unauthenticated(self):
        with self.client:
            self.login_managerA()
            res = self.send_hide_request(False)

            # TODO
