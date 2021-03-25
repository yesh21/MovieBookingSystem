# Fix being within folder
import sys
import os
sys.path.insert(0, os.path.dirname(__file__) + '/..')

from Flask_Cinema_Site import db
from Flask_Cinema_Site.models import Movie, Viewing, Seat

from datetime import date, datetime, timedelta

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

m3 = Movie(
    name='Tenet',
    overview='Armed with only one word, Tenet, and fighting for the survival of the entire world '
             'Protagonist journeys through a twilight world of international espionage '
             'on a mission that will unfold in something beyond real time. '
             'The film is written by Christorpher Nolan',
    released=date(2020, 6, 11),
    cover_art_name='tent.jpg',
    directors='Jason Reitman',
    cast='Juhan Ulfsak, Jefferson Hall, Ivo Uukkivi, Andrew Howard, Ernie Hudson',
    duration=125,
    rating=4.0,
    hidden=False
)

db.session.add(m3)

m4 = Movie(
    name='The Dig',
    overview='In the late 1930s, wealthy landowner Edith Pretty hires amateur '
             'archaeologist Basil Brown to investigate the mounds on her property '
             'in England. He and his team discover a ship from the Dark Ages while digging up a burial ground. '
             'The film is written by John Preston',
    released=date(2020, 8, 11),
    cover_art_name='dig.jpg',
    directors='Simon Stone',
    cast='Lily Jame, Ralph Fiennes, Carey Mulligan, Johnny Flynn, Ben Chaplin',
    duration=140,
    rating=4.0,
    hidden=False
)

db.session.add(m3)
db.session.commit()

# Add some times for each movie
viewing_times = [
    datetime.today().replace(hour=10, minute=0, second=0, microsecond=0),
    datetime.today().replace(hour=14, minute=15, second=0, microsecond=0),
    datetime.today().replace(hour=17, minute=30, second=0, microsecond=0),
    datetime.today().replace(hour=19, minute=20, second=0, microsecond=0),
    datetime.today().replace(hour=20, minute=45, second=0, microsecond=0)
]

for m in Movie.query.all():
    # Add viewings for the next 14 days
    for day_num in range(14):
        for viewing_time in viewing_times:
            m.viewings.append(Viewing(
                time=viewing_time + timedelta(days=day_num, minutes=20 * day_num),
                price=5.50
            ))

        # Add extra same time viewings on fridays
        if (datetime.today() + timedelta(days=day_num)).weekday() == 4:
            m.viewings.append(Viewing(
                time=viewing_times[2] + timedelta(days=day_num, minutes=20 * day_num),
                price=4.40
            ))

            m.viewings.append(Viewing(
                time=viewing_times[-1] + timedelta(days=day_num, minutes=20 * day_num),
                price=7.77
            ))

db.session.commit()

# For each viewing add some seats
for v in Viewing.query.all():
    for i in range(20):
        v.seats.append(Seat(
            seat_number=f'A{i}'
        ))

db.session.commit()
