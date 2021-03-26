from Tests.movie.base_movie import MovieBaseTestCase

from Flask_Cinema_Site import db
from Flask_Cinema_Site.models import Viewing

from flask import url_for

from datetime import date, timedelta
from sqlalchemy import func


class ViewSpecificMovieTestCase(MovieBaseTestCase):
    # Success
    def test_view_specific_details(self):
        with self.client:
            res = self.client.get(url_for('movie.view_specific', movie_id=self.movie_A.id))

            self.assert200(res)

            # Check movie details
            self.assertIn(self.movie_A.name.encode(), res.data)
            self.assertIn(self.movie_A.overview.encode(), res.data)
            self.assertIn(self.movie_A.cover_art_name.encode(), res.data)
            self.assertIn(self.movie_A.directors.encode(), res.data)
            self.assertIn(self.movie_A.cast.encode(), res.data)
            self.assertIn(self.movie_A.genres.encode(), res.data)

            self.assertIn(self.movie_A.released.strftime("%B %d, %Y").encode(), res.data)
            self.assertIn(str(self.movie_A.duration).encode(), res.data)

            # Check movie viewings
            viewings = Viewing.query\
                .filter(Viewing.movie_id == self.movie_A.id)\
                .filter(func.date(Viewing.time) >= date.today())\
                .filter(func.date(Viewing.time) <= date.today() + timedelta(days=6))\
                .all()
            for v in viewings:
                self.assertIn(v.time.strftime("%H:%M").encode('utf-8'), res.data)
                self.assertIn(f'viewing/{v.id}'.encode('utf-8'), res.data)

    def test_view_specific_buttons_manager(self):
        with self.client:
            self.login_managerA()
            res = self.client.get(url_for('movie.view_specific', movie_id=self.movie_A.id))

            self.assert200(res)

            self.assertIn(b'Edit movie', res.data)
            self.assertIn(b'Hide movie', res.data)
            self.assertIn(b'Show movie', res.data)
            self.assertIn(b'Delete movie', res.data)

    def test_view_specific_hidden_manager(self):
        with self.client:
            self.login_managerA()
            self.movie_A.hidden = True
            db.session.commit()
            res = self.client.get(url_for('movie.view_specific', movie_id=self.movie_A.id))

            self.assert200(res)

    # Fail
    def test_view_specific_non_existent(self):
        with self.client:
            res = self.client.get(url_for('movie.view_specific', movie_id=999))

            self.assert404(res)

    def view_specific_asset_no_buttons(self):
        res = self.client.get(url_for('movie.view_specific', movie_id=self.movie_A.id))

        self.assert200(res)

        self.assertNotIn(b'Edit movie', res.data)
        self.assertNotIn(b'Hide movie', res.data)
        self.assertNotIn(b'Show movie', res.data)
        self.assertNotIn(b'Delete movie', res.data)

    def test_view_specific_buttons_customer(self):
        with self.client:
            self.login_customerA()
            self.view_specific_asset_no_buttons()

    def test_view_specific_buttons_unauthenticated(self):
        with self.client:
            self.view_specific_asset_no_buttons()

    def test_view_specific_hidden_customer(self):
        with self.client:
            self.movie_A.hidden = True
            db.session.commit()

            self.login_customerA()
            res = self.client.get(url_for('movie.view_specific', movie_id=self.movie_A.id))
            self.assert404(res)

    def test_view_specific_hidden_unauthenticated(self):
        with self.client:
            self.movie_A.hidden = True
            db.session.commit()

            res = self.client.get(url_for('movie.view_specific', movie_id=self.movie_A.id))
            self.assert404(res)
