import os
from app import create_app, db
from app.users.models import Users
from flask.ext.script import Manager, Shell


app = create_app('dev')
manager = Manager(app)

def make_shell_context():
    return dict(app=app, db=db, Users=Users)


manager.add_command("shell",Shell(make_context=make_shell_context))


if __name__ == '__main__':

    manager.run()