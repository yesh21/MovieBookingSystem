from Tests.movie.base_movie import MovieBaseTestCase

from flask import url_for


class AddMovieTestCase(MovieBaseTestCase):
    # GET
    def test_add_movie_get_manager(self):
        with self.client:
            self.login_managerA()
            res = self.client.get(url_for('movie.add'))
            self.assert200(res)
            self.assertIn(b'Add Movie', res.data)

    def test_add_movie_get_customer(self):
        with self.client:
            self.login_customerA()

            res = self.client.get(url_for('movie.add'))
            self.assert401(res)

    def test_add_movie_get_unauthenticated(self):
        with self.client:
            res = self.client.get(url_for('movie.add'))
            self.assert401(res)

    # POST
    def test_add_movie_post_manager(self):
        with self.client:
            num_movies = self.get_num_movies()
            self.login_managerA()

            params = self.get_correct_movie_params()
            res = self.client.post(url_for('movie.add'), data=params, follow_redirects=True)

            self.assert200(res)
            self.assert_message_flashed(f'Movie \'{params["name"]}\' added successfully', 'success')
            self.assert_movie_with_params_in_db(params)
            self.assertEqual(num_movies + 1, self.get_num_movies())

    def test_add_movie_post_customer(self):
        with self.client:
            num_movies = self.get_num_movies()
            self.login_customerA()

            params = self.get_correct_movie_params()
            res = self.client.post(url_for('movie.add'), data=params, follow_redirects=True)

            self.assert401(res)
            self.assertEqual(num_movies, self.get_num_movies())

    def test_add_movie_post_unauthenticated(self):
        with self.client:
            num_movies = self.get_num_movies()

            params = self.get_correct_movie_params()
            res = self.client.post(url_for('movie.add'), data=params, follow_redirects=True)

            self.assert401(res)
            self.assertEqual(num_movies, self.get_num_movies())

    def test_add_movie_post_manager_invalid(self):
        with self.client:
            num_movies = self.get_num_movies()
            self.login_managerA()

            params = self.get_invalid_movie_params()
            res = self.client.post(url_for('movie.add'), data=params, follow_redirects=True)

            self.assert400(res)
            self.assertIn(b'Field must be between 5 and 100 characters long.', res.data)
            self.assertIn(b'This field is required.', res.data)
            self.assertIn(b'File does not have an approved extension: jpg, jpeg, png', res.data)

            self.assertEqual(num_movies, self.get_num_movies())

    def test_add_movie_post_manager_no_csrf(self):
        with self.client:
            num_movies = self.get_num_movies()
            self.login_managerA()

            params = self.get_correct_movie_params()
            del(params['csrf_token'])
            res = self.client.post(url_for('movie.add'), data=params, follow_redirects=True)

            self.assert400(res)
            self.assertEqual(num_movies, self.get_num_movies())
