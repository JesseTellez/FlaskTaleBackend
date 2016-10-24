#MANGER TO START APPLICATION

from app import create_app, db
from app.models import User, Story, Genre, Addition
from flask.ext.script import Manager, Shell
#This will be for later migration stuff
from flask.ext.migrate import Migrate, MigrateCommand
from .cofig import Default

#change this
app = create_app()

manager = Manager(app)

def make_shell_context():
    return dict(app=app, db=db, User=User, Story=Story, Genre=Genre, Addition=Addition)
    
manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()