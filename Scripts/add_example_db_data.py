# Fix being within folder
import sys
import os

sys.path.insert(0, os.path.dirname(__file__) + '/..')

from Flask_Cinema_Site import db
from Flask_Cinema_Site.models import Movie, Viewing, Seat, Transaction, User, Role, TicketType, SavedCard, Screen

from datetime import date, datetime, timedelta

# Add a customer account
customer_role = Role.query.filter_by(name='customer').first()
customer_A = User(
    username='CustomerA',
    first_name='First',
    last_name='Last',
    email='customerA@example.com',
    confirmed=True
)
customer_A.set_password('customerA')
customer_role.users.append(customer_A)

# Add a manager account
manager_role = Role.query.filter_by(name='manager').first()
manager_A = User(
    username='ManagerA',
    first_name='First',
    last_name='Last',
    email='managerA@example.com',
    confirmed=True
)
manager_A.set_password('managerA')
manager_role.users.append(manager_A)

# Add a admin / manager account
admin_role = Role.query.filter_by(name='admin').first()
admin_A = User(
    username='AdminA',
    first_name='First',
    last_name='Last',
    email='adminA@example.com',
    confirmed=True
)
admin_A.set_password('adminA')

admin_role.users.append(admin_A)
manager_role.users.append(admin_A)

db.session.commit()
# genres so far; Action, Drama, Space, Fantasy

# Add card to manager
manager_A.saved_cards.append(SavedCard(
    number='1234 5678 1234 5678',
    expiry=date.today()
))
manager_A.saved_cards.append(SavedCard(
    number='9876 5432 2198 7654',
    expiry=date.today() + timedelta(days=7)
))
db.session.commit()

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
    hidden=False,
    genres="Action",
    trailer="https://www.youtube.com/embed/Fp9pNPdNwjI"
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
    hidden=True,
    genres="Action",
    trailer="https://www.youtube.com/embed/ahZFCF--uRY"
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
    hidden=False,
    genres="Action",
    trailer="https://www.youtube.com/embed/L3pk_TBkihU"
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
    hidden=False,
    genres="Drama",
    trailer="https://www.youtube.com/embed/JZQz0rkNajo"
)

db.session.add(m4)

m5 = Movie(
    name='LockedDown',
    overview='Just as they decide to separate, Linda and Paxton find life has other'
             'plans when they are stuck at home in a mandatory lockdown. '
             'Co-habitation is proving to be a challenge,  '
             'but it will bring them closer together in the most surprising way.',
    released=date(2020, 9, 11),
    cover_art_name='lock.jpg',
    directors='Doug Liman',
    cast='Anne Hathaway, Chiwetel Ejiofor, Lucy Boynton, Jazmyn Simon, Dule Hill',
    duration=140,
    rating=3.5,
    hidden=False,
    genres="Action",
    trailer="https://www.youtube.com/embed/mepeWor5JPk"
)

db.session.add(m5)

m6 = Movie(
    name='Inception',
    overview='Cobb steals information from his targets by entering their dreams.'
             'Saito offers to wipe clean Cobbs criminal history as payment for '
             'performing an inception on his sick competitors son.  ',
    released=date(2010, 9, 11),
    cover_art_name='inception.jpg',
    directors='Christopher Nolan',
    cast='Leonardo DiCaprio, Joseph Gordon-Levitt, Tom Hardy, Cillian Murphy, Marion Cotillard',
    duration=160,
    rating=4.5,
    hidden=False,
    genres="Action",
    trailer="https://www.youtube.com/embed/YoHD9XEInc0"
)

db.session.add(m6)

m7 = Movie(
    name='The Martian',
    overview='When astronauts blast off from the planet Mars, they leave behind'
             'Mark Watney (Matt Damon), presumed dead after a fierce storm.'
             'With only a meager amount of supplies, the stranded visitor must '
             'utilize his wits and spirit to find a way to survive'
             '(also the managers favourite movie!)',
    released=date(2015, 10, 9),
    cover_art_name='martian.jpg',
    directors='Ridley Scott',
    cast='Matt Damon, Jessica Chastain, Kate Mara Beth, Chiwetel Ejiofor, Jeff Daniels',
    duration=120,
    rating=5.0,
    hidden=False,
    genres="Space",
    trailer="https://www.youtube.com/embed/ej3ioOneTy8"
)

db.session.add(m7)

m8 = Movie(
    name='The Lord of the Rings: The Fellowship of the Ring',
    overview='A young hobbit, Frodo, who has found the One Ring that belongs to'
             'the Dark Lord Sauron, begins his journey with eight companions to'
             'Mount Doom, the only place where it can be destroyed.',
    released=date(2001, 10, 9),
    cover_art_name='lotr.jpg',
    directors='Peter Jackson',
    cast='Sala Baker, Viggo Mortensen, Elijah Wood, Orlando Bloom, Ian Mckellen',
    duration=160,
    rating=5.0,
    hidden=False,
    genres="Fantasy",
    trailer="https://www.youtube.com/embed/V75dMMIW2B4"
)

db.session.add(m8)
db.session.commit()

# Add some times for each movie
viewing_times = [
    datetime.today().replace(hour=14, minute=15, second=0, microsecond=0),
    datetime.today().replace(hour=17, minute=30, second=0, microsecond=0),
    datetime.today().replace(hour=19, minute=20, second=0, microsecond=0),
    datetime.today().replace(hour=20, minute=45, second=0, microsecond=0)
]

# For simplicity give each movie its own screen
screen_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                  'U', 'V', 'W', 'X', 'Y', 'Z']

for m, screen_letter in zip(Movie.query.all(), screen_letters):
    screen = Screen(name=screen_letter)
    db.session.add(screen)
    db.session.commit()

    # Add viewings for the next 7 days
    for day_num in range(7):
        for viewing_time in viewing_times:
            v = Viewing(
                time=viewing_time + timedelta(days=day_num, minutes=20 * day_num),
                screen_id=screen.id
            )
            v.init_seats()
            m.viewings.append(v)

db.session.commit()


def book_seats(seat_nums, t, v_id):
    child_ticket_type = TicketType.query.filter_by(name='Child').first()
    adult_ticket_type = TicketType.query.filter_by(name='Adult').first()
    senior_ticket_type = TicketType.query.filter_by(name='Senior').first()

    for seat_num, ticket_type in seat_nums:
        seat = Seat.query.filter_by(viewing_id=v_id, seat_number=seat_num, transaction_id=None).first()
        if not seat:
            print(f'Seat already {seat_num} booked')
            break

        if ticket_type == 'Child':
            child_ticket_type.seats.append(seat)
        elif ticket_type == 'Senior':
            senior_ticket_type.seats.append(seat)
        elif ticket_type == 'Adult':
            adult_ticket_type.seats.append(seat)
        else:
            print('Invalid ticket type')
            break

        t.seats.append(seat)


seat_numbers = [('B3', 'Child'), ('B4', 'Adult'), ('B6', 'Senior')]

# Commented out cause they won't have receipts
# book_seats(seat_numbers, Transaction(user_id=2), 1)
# book_seats(seat_numbers, Transaction(user_id=3), 2)


db.session.commit()
