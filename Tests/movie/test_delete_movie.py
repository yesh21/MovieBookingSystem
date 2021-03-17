from Tests.movie.base_movie import MovieBaseTestCase

from Flask_Cinema_Site.models import Movie

from flask import url_for
from flask_api import status


class DeleteMovieTestCase(MovieBaseTestCase):
    # Success
    def test_delete_movie_manager(self):
        with self.client:
            num_movies = self.get_num_movies()
            self.login_managerA()

            params = dict(
                id=self.movie_A.id,
                csrf_token=self.csrf_token
            )
            res = self.client.post(url_for('movie.delete'), data=params, follow_redirects=True)

            self.assert_json_response(res, f'Movie with id \'{params["id"]}\' successfully deleted', status.HTTP_200_OK)
            self.assertEqual(num_movies - 1, self.get_num_movies())

            # Check movie was deleted
            m = Movie.query.get(self.movie_A.id)
            self.assertIsNone(m)

    # Fail
    def test_delete_movie_customer(self):
        with self.client:
            num_movies = self.get_num_movies()
            self.login_customerA()

            params = dict(
                id=self.movie_A.id,
                csrf_token=self.csrf_token
            )
            res = self.client.post(url_for('movie.delete'), data=params, follow_redirects=True)

            self.assert401(res)
            self.assertEqual(num_movies, self.get_num_movies())

    def test_delete_movie_unauthenticated(self):
        with self.client:
            num_movies = self.get_num_movies()

            params = dict(
                id=self.movie_A.id,
                csrf_token=self.csrf_token
            )
            res = self.client.post(url_for('movie.delete'), data=params, follow_redirects=True)

            self.assert401(res)
            self.assertEqual(num_movies, self.get_num_movies())

    def test_delete_movie_non_existent(self):
        with self.client:
            num_movies = self.get_num_movies()
            self.login_managerA()

            params = dict(
                id=999,
                csrf_token=self.csrf_token
            )
            res = self.client.post(url_for('movie.delete'), data=params, follow_redirects=True)

            self.assert_json_response(res, 'Movie with id \'999\' not found', status.HTTP_400_BAD_REQUEST)
            self.assertEqual(num_movies, self.get_num_movies())

    def test_delete_movie_missing_movie_id(self):
        with self.client:
            num_movies = self.get_num_movies()
            self.login_managerA()

            params = dict(
                csrf_token=self.csrf_token
            )
            res = self.client.post(url_for('movie.delete'), data=params, follow_redirects=True)

            self.assert_json_response(res, 'Delete movie failed', status.HTTP_400_BAD_REQUEST)
            self.assertEqual(num_movies, self.get_num_movies())

    def test_delete_movie_no_csrf(self):
        with self.client:
            num_movies = self.get_num_movies()
            self.login_managerA()

            params = dict(
                id=self.movie_A.id
            )
            res = self.client.post(url_for('movie.delete'), data=params, follow_redirects=True)

            self.assert_json_response(res, 'Delete movie failed', status.HTTP_400_BAD_REQUEST)
            self.assertEqual(num_movies, self.get_num_movies())

            # Check movie still in db
            m = Movie.query.get(self.movie_A.id)
            self.assertIsNotNone(m)
