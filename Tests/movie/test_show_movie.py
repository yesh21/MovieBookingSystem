from Tests.movie.base_movie import MovieBaseTestCase

from Flask_Cinema_Site import db

from flask import url_for
from flask_api import status


class ShowMovieTestCase(MovieBaseTestCase):
    def send_show_request(self, hidden):
        self.movie_A.hidden = hidden
        db.session.commit()

        params = dict(
            id=self.movie_A.id,
            csrf_token=self.csrf_token
        )
        return self.client.post(url_for('movie.show'), data=params, follow_redirects=True)

    # Success
    def test_show_hidden_movie_manager(self):
        with self.client:
            self.login_managerA()
            res = self.send_show_request(True)

            self.assert_json_response(res, f'Movie with id \'{self.movie_A.id}\' successfully unhidden',
                                      status.HTTP_200_OK)
            self.assertEqual(self.movie_A.hidden, False)

    def test_show_visible_movie_manager(self):
        with self.client:
            self.login_managerA()
            res = self.send_show_request(False)

            self.assert_json_response(res, f'Movie with id \'{self.movie_A.id}\' successfully unhidden',
                                      status.HTTP_200_OK)
            self.assertEqual(self.movie_A.hidden, False)

    # Fail
    def test_show_movie_non_existent(self):
        with self.client:
            self.login_managerA()

            params = dict(
                id=999,
                csrf_token=self.csrf_token
            )
            res = self.client.post(url_for('movie.show'), data=params, follow_redirects=True)

            self.assert_json_response(res, 'Movie with id \'999\' not found', status.HTTP_400_BAD_REQUEST)

    def test_show_hidden_movie_no_id(self):
        with self.client:
            self.login_managerA()
            self.movie_A.hidden = True
            db.session.commit()

            params = dict(
                csrf_token=self.csrf_token
            )
            res = self.client.post(url_for('movie.show'), data=params, follow_redirects=True)

            self.assert_json_response(res, 'Error show movie failed', status.HTTP_400_BAD_REQUEST)
            self.assertEqual(self.movie_A.hidden, True)

    def test_show_hidden_movie_no_csrf(self):
        with self.client:
            self.login_managerA()
            self.movie_A.hidden = True
            db.session.commit()

            params = dict(
                id=self.movie_A.id
            )
            res = self.client.post(url_for('movie.show'), data=params, follow_redirects=True)

            self.assert_json_response(res, 'Error show movie failed', status.HTTP_400_BAD_REQUEST)
            self.assertEqual(self.movie_A.hidden, True)

    def test_show_hidden_movie_customer(self):
        with self.client:
            self.login_customerA()
            res = self.send_show_request(True)

            self.assert401(res)
            self.assertEqual(self.movie_A.hidden, True)

    def test_show_hidden_movie_unauthenticated(self):
        with self.client:
            res = self.send_show_request(True)

            self.assert401(res)
            self.assertEqual(self.movie_A.hidden, True)
