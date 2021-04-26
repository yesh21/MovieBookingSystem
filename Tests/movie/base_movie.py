from Tests.base import BaseTestCase

from Flask_Cinema_Site import db
from Flask_Cinema_Site.models import Movie

from datetime import date
from sqlalchemy import func


class MovieBaseTestCase(BaseTestCase):
    def get_num_movies(self):
        return db.session.query(func.count(Movie.id)).scalar()

    def get_movie_params_from_model(self, m: Movie):
        return dict(
            name=m.name,
            overview=m.overview,
            released=m.released,
            duration=m.duration,
            rating=m.rating,
            directors=m.directors,
            cast_list=m.cast,
            genres=m.genres,
            trailer=m.trailer,
            picture=self.get_file_parameter('ghostbusters.jpg'),
            csrf_token=self.csrf_token
        )

    def get_correct_movie_params(self):
        return dict(
            name='valid movie name',
            overview='overview of movie',
            released=date.today(),
            duration=123,
            rating=3,
            trailer='a youtube link',
            directors='a director',
            cast_list='a actor, another actor',
            genres='comedy',
            picture=self.get_file_parameter('ghostbusters.jpg'),
            csrf_token=self.csrf_token
        )

    def get_invalid_movie_params(self):
        return dict(
            name='N',
            overview='o',
            released='not a date',
            duration='not a number',
            rating=9,
            trailer='X',
            directors='',
            cast_list='',
            genres='',
            picture=self.get_file_parameter('text_file.txt'),
            csrf_token=self.csrf_token
        )

    def get_movie_from_params(self, params):
        return Movie.query.filter_by(
            name=params['name'],
            overview=params['overview'],
            released=params['released'],
            duration=params['duration'],
            rating=params['rating'],
            directors=params['directors'],
            cast=params['cast_list'],
            trailer=params['trailer'],
            genres=params['genres']
        ).first()

    def assert_movie_with_params_in_db(self, params):
        m = self.get_movie_from_params(params)
        self.assertIsNotNone(m)
        self.assertIsNotNone(m.cover_art_name)

    def assert_movie_with_params_not_in_db(self, params):
        m = self.get_movie_from_params(params)
        self.assertIsNone(m)
