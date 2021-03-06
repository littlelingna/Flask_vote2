import os
from flask_script import Manager, Shell
from app import create_app, db
from app.models import User, Action
from flask_migrate import Migrate, MigrateCommand, upgrade

app = create_app('default')
manager = Manager(app)
# migrate = Migrate(app, db)
####  addded for remote visit
app.host='0.0.0.0'

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Action)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
