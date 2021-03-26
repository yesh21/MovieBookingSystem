# Fix being within folder
import sys
import os
sys.path.insert(0, os.path.dirname(__file__) + '/..')

from Flask_Cinema_Site import db
from Flask_Cinema_Site.models import Role, TicketType

db.create_all()

# Add roles
db.session.add(Role(name='admin'))
db.session.add(Role(name='manager'))
db.session.add(Role(name='customer'))

# Add ticket types
db.session.add(TicketType(name='Child', price=4.50))
db.session.add(TicketType(name='Senior', price=5.50))
db.session.add(TicketType(name='Adult', price=6.50))
db.session.add(TicketType(name='Vip', price=8.00))

db.session.commit()
