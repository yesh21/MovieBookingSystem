from Flask_Cinema_Site import app, db
from Flask_Cinema_Site.models import *

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

migrate = Migrate(app, db, render_as_batch=True)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
