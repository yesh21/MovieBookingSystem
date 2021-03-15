from Tests.movie.base_movie import MovieBaseTestCase

from Flask_Cinema_Site.models import Movie

from flask import url_for


class ViewAllMoviesTestCase(MovieBaseTestCase):
    def test_view_multiple_movies_visible(self):
        with self.client:
            # Set all movies visible
            Movie.query.update({Movie.hidden: False})

            res = self.client.get(url_for('movie.view_multiple'))
            self.assert200(res)
            self.assertIn(b'Browse Movies', res.data)

            for m in Movie.query.all():
                self.assertIn(m.name.encode('utf-8'), res.data)
                self.assertIn(m.cover_art_name.encode('utf-8'), res.data)

    def test_view_multiple_movies_hidden(self):
        with self.client:
            # Set all movies hidden
            Movie.query.update({Movie.hidden: True})

            res = self.client.get(url_for('movie.view_multiple'))
            self.assert200(res)
            self.assertIn(b'Browse Movies', res.data)

            for m in Movie.query.all():
                self.assertNotIn(m.name.encode('utf-8'), res.data)
                self.assertNotIn(m.cover_art_name.encode('utf-8'), res.data)
