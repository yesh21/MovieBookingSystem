# Fix being within folder
import sys
import os
sys.path.insert(0, os.path.dirname(__file__) + '/..')

from Flask_Cinema_Site import db

db.create_all()
