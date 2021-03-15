from Tests.movie.base_movie import MovieBaseTestCase

from Flask_Cinema_Site.models import Movie

from flask import url_for


class ManageMoviesTestCase(MovieBaseTestCase):
    # Success
    def test_view_specific_details_manager(self):
        with self.client:
            self.login_managerA()
            res = self.client.get(url_for('movie.manage'))

            self.assert200(res)

            for m in Movie.query.all():
                # Check movie details
                self.assertIn(m.name.encode(), res.data)
                self.assertIn(m.released.strftime("%B %d, %Y").encode(), res.data)
                self.assertIn(str(m.duration).encode(), res.data)

                # Check movie links
                self.assertIn(url_for('movie.view_specific', movie_id=m.id).encode('utf-8'), res.data)
                self.assertIn(url_for('movie.edit', movie_id=m.id).encode('utf-8'), res.data)

    def test_view_specific_details_customer(self):
        with self.client:
            self.login_customerA()
            res = self.client.get(url_for('movie.manage'))

            # TODO

    def test_view_specific_details_unauthenticated(self):
        with self.client:
            res = self.client.get(url_for('movie.manage'))

            # TODO
