from Tests.movie.base_movie import MovieBaseTestCase

from flask import url_for


class EditMovieTestCase(MovieBaseTestCase):
    # GET
    # Success
    def test_edit_movie_get_manager(self):
        with self.client:
            self.login_managerA()
            res = self.client.get(url_for('movie.edit', movie_id=self.mA.id))
            self.assert200(res)
            self.assertIn(b'Edit Movie', res.data)

    # Fail
    def test_edit_movie_get_customer(self):
        with self.client:
            self.login_customerA()
            # TODO
            pass

    def test_edit_movie_get_unauthenticated(self):
        with self.client:
            # TODO
            pass

    def test_edit_movie_get_non_existent(self):
        with self.client:
            self.login_managerA()
            res = self.client.get(url_for('movie.edit', movie_id=999))
            self.assert404(res)
            self.assert_message_flashed('Movie with id \'999\' does not exist', 'danger')

    # POST
    # Success
    def test_edit_movie_post_manager(self):
        with self.client:
            num_movies = self.get_num_movies()
            self.login_managerA()

            params = self.get_correct_movie_params()
            res = self.client.post(url_for('movie.edit', movie_id=self.mA.id), data=params, follow_redirects=True)

            self.assert200(res)
            self.assert_movie_with_params_in_db(params)
            self.assertEqual(num_movies, self.get_num_movies())
            self.assert_message_flashed(f'Movie \'{params["name"]}\' saved successfully', 'success')

    # Fail
    def test_edit_movie_post_customer(self):
        with self.client:
            num_movies = self.get_num_movies()
            self.login_customerA()

            params = self.get_correct_movie_params()
            res = self.client.post(url_for('movie.edit', movie_id=self.mA.id), data=params, follow_redirects=True)

            # TODO
            self.assertEqual(num_movies, self.get_num_movies())

    def test_edit_movie_post_unauthenticated(self):
        with self.client:
            num_movies = self.get_num_movies()

            params = self.get_correct_movie_params()
            res = self.client.post(url_for('movie.edit', movie_id=self.mA.id), data=params, follow_redirects=True)

            # TODO
            self.assertEqual(num_movies, self.get_num_movies())

    def test_edit_movie_post_manager_invalid(self):
        with self.client:
            num_movies = self.get_num_movies()
            self.login_managerA()

            params = self.get_invalid_movie_params()
            res = self.client.post(url_for('movie.edit', movie_id=self.mA.id), data=params, follow_redirects=True)

            self.assert400(res)
            self.assertIn(b'Field must be between 5 and 100 characters long.', res.data)
            self.assertIn(b'This field is required.', res.data)

            self.assert_movie_with_params_not_in_db(params)
            self.assertEqual(num_movies, self.get_num_movies())

    def test_edit_movie_post_manager_no_csrf(self):
        with self.client:
            num_movies = self.get_num_movies()
            self.login_managerA()

            params = self.get_correct_movie_params()
            del(params['csrf_token'])
            res = self.client.post(url_for('movie.edit', movie_id=self.mA.id), data=params, follow_redirects=True)

            self.assert400(res)
            self.assert_movie_with_params_not_in_db(params)
            self.assertEqual(num_movies, self.get_num_movies())
