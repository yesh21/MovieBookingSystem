from Flask_Cinema_Site import db
from Flask_Cinema_Site.models import Viewing, Seat, User, Transaction

# Example user
current_user = User.query.first()

# Given the viewing id
viewing_id = 1

available_seats = Seat.query.filter_by(viewing_id=viewing_id, transaction_id=None)

new_transaction = Transaction()
current_user.transactions.append(new_transaction)

new_transaction.seats.append(available_seats[0])
new_transaction.seats.append(available_seats[1])

db.session.commit()

print('Test')
