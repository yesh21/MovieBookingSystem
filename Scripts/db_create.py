# Fix being within folder
import sys
import os
sys.path.insert(0, os.path.dirname(__file__) + '/..')

from Flask_Cinema_Site import db
from Flask_Cinema_Site.models import Role

db.create_all()

# Add roles
db.session.add(Role(name='admin'))
db.session.add(Role(name='manager'))
db.session.add(Role(name='customer'))

db.session.commit()
