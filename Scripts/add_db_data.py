# Fix being within folder
import sys
import os
sys.path.insert(0, os.path.dirname(__file__) + '/..')

from Flask_Cinema_Site import db
from Flask_Cinema_Site.models import Movie, Viewing, Seat, Transaction, User, Role, TicketType

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

# Add some times for each movie
viewing_times = [
    # datetime.today().replace(hour=10, minute=0, second=0, microsecond=0),
    # datetime.today().replace(hour=14, minute=15, second=0, microsecond=0),
    datetime.today().replace(hour=17, minute=30, second=0, microsecond=0),
    datetime.today().replace(hour=19, minute=20, second=0, microsecond=0),
    datetime.today().replace(hour=20, minute=45, second=0, microsecond=0)
]

for m in Movie.query.all():
    # Add viewings for the next 2 days
    for day_num in range(2):
        for viewing_time in viewing_times:
            m.viewings.append(Viewing(
                time=viewing_time + timedelta(days=day_num, minutes=20 * day_num),
                price=5.50
            ))

        # Add extra same time viewings on fridays
        if (datetime.today() + timedelta(days=day_num)).weekday() == 4:
            m.viewings.append(Viewing(
                time=viewing_times[1] + timedelta(days=day_num, minutes=20 * day_num),
                price=4.40
            ))

            m.viewings.append(Viewing(
                time=viewing_times[-1] + timedelta(days=day_num, minutes=20 * day_num),
                price=7.77
            ))

db.session.commit()

# For each viewing add some seats
for v in Viewing.query.all():
    for char in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']:
        for i in range(1, 10):
            v.seats.append(Seat(
                seat_number=char + str(i)
            ))

db.session.commit()


# Book seats for viewing 1
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

book_seats(seat_numbers, Transaction(user_id=2), 1)
book_seats(seat_numbers, Transaction(user_id=3), 2)


db.session.commit()
