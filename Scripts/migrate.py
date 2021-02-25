# Fix being within folder
import sys
import os
sys.path.insert(0, os.path.dirname(__file__) + '/..')
os.chdir(os.path.dirname(__file__) + '/..')

from Flask_Cinema_Site import app, db
# from Flask_Cinema_Site.models import *

# from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

migrate = Migrate(app, db, render_as_batch=True)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
