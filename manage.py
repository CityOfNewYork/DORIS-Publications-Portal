import subprocess

from flask_script import Manager, Server, Shell

from config import DEV
from app import create_app
from app.database import db
from app.models import AuthUser

manager = Manager(create_app(DEV))


@manager.command
def create_user():
    pass

# runserver ------------------------------------------------------------------------------------------------------------

class ServerWithRedis(Server):
    """
    Same as flask_script.Server but also starts redis if not running in RedHat environment.
    """
    def __init__(self):
        super(ServerWithRedis, self).__init__()
        try:
            subprocess.check_output(['pgrep', 'redis'])
        except subprocess.CalledProcessError:
            subprocess.call(['sudo', 'service', 'rh-redis32', 'redis', 'start'])  # TODO: test


manager.add_command("runserver", ServerWithRedis())

# shell ----------------------------------------------------------------------------------------------------------------

def make_shell_context():
    from flask import current_app
    return dict(
        current_app=current_app,
        db=db,
    )

manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == "__main__":
    manager.run()
