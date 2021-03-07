# Fix being within folder
import sys
import os
sys.path.insert(0, os.path.dirname(__file__) + '/..')

from Flask_Cinema_Site import db
from Flask_Cinema_Site.models import Movie, Viewing
from itertools import cycle

from datetime import date, datetime

m1 = Movie(
    name='Black Widow',
    overview='In Marvel Studios’ action-packed spy thriller “Black Widow,” '
             'Natasha Romanoff aka Black Widow confronts the darker parts of '
             'her ledger when a dangerous conspiracy with ties to her past '
             'arises. Pursued by a force that will stop at nothing to bring '
             'her down, Natasha must deal with her history as a spy and the '
             'broken relationships left in her wake long before she became an Avenger.',
    released=date(2021, 5, 7),
    cover_art_name='black_widow.jpg',
    directors='Cate Shortland',
    cast='Rachel Weisz, David Harbour, O-T Fagbenle, Ray Winstone, Florence '
         'Pugh, Scarlett Johansson',
    duration=123,
    rating=4.2,
    hidden=True
)
db.session.add(m1)

m2 = Movie(
    name='Ghostbusters: Afterlife',
    overview='From director Jason Reitman and producer Ivan Reitman, comes the next chapter '
             'in the original Ghostbusters universe. In Ghostbusters: Afterlife, when a single '
             'mom and her two kids arrive in a small town, they begin to discover their connection '
             'to the original ghostbusters and the secret legacy their grandfather left behind. '
             'The film is written by Jason Reitman & Gil Kenan.',
    released=date(2021, 6, 11),
    cover_art_name='ghostbusters.jpg',
    directors='Jason Reitman',
    cast='Finn Wolfhard, Bill Murray, Dan Aykroyd, Sigourney Weaver, Ernie Hudson, Paul Rudd, '
         'McKenna Grace, Carrie Coon, Bokeem Woodbine, Annie Potts',
    duration=125,
    rating=3.5,
    hidden=False
)

db.session.add(m2)
db.session.commit()

# Add random times for each movie id
Movies = Movie.query.all()
hourShowing = [10, 12, 14, 16, 18]
minuteShowing = [15, 45]

cycleHour = cycle(hourShowing)
cycleMinute = cycle(minuteShowing)
viewingTimes = []
for i in range(len(Movies)):
    viewingTimes.append(datetime(2012, 3, 3, next(cycleHour), next(cycleMinute)))

for count, movie in enumerate(Movies):
    viewing1 = Viewing(movie_id=movie.id, time=viewingTimes[count])
    db.session.add(viewing1)

db.session.commit()
