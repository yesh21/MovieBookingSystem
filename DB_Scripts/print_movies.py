# Fix being within folder
import sys
import os
sys.path.insert(0, os.path.dirname(__file__) + '/..')

from Flask_Cinema_Site import db
from Flask_Cinema_Site.models import Movie

print('Movies')
for m in Movie.query.all():
    print(f'{m.name} - {m.id}')
