import subprocess

from flask_script import Manager, Server, Shell

from config import DEV
from app import create_app
from app.database import db, user

app = create_app(DEV)
manager = Manager(app)

# recreate_tables ------------------------------------------------------------------------------------------------------

@manager.command
def recreate_tables():
    db.drop_all()
    db.create_all()

# create_user ----------------------------------------------------------------------------------------------------------

@manager.command
def create_user(first_name, last_name, middle_initial=None, email=None):
    from app.constants import user_auth_type
    user.create(
        "generate_guid",
        user_auth_type.NYC_ID,
        first_name,
        middle_initial,
        last_name,
        "{}{}@email.com".format(first_name[0], last_name)
    )


# runserver ------------------------------------------------------------------------------------------------------------

class ServerWithRedis(Server):
    """
    Same as flask_script.Server but also starts the redis service.
    """

    def __init__(self):
        super(ServerWithRedis, self).__init__()
        try:
            subprocess.check_output(['pgrep', 'redis'])
        except subprocess.CalledProcessError:
            subprocess.call(['sudo', 'service', 'rh-redis32-redis', 'start'])


manager.add_command("runserver", ServerWithRedis())


# shell ----------------------------------------------------------------------------------------------------------------

def make_shell_context():
    from flask import current_app
    from app import models, database
    return dict(
        current_app=current_app,
        db=db,
        database=database,
        models=models
    )


manager.add_command("shell", Shell(make_context=make_shell_context))

# TODO: REMOVE ME. This is a proof of concept only
@manager.command
def generate_schema():
    import json
    from app.models.schema import Schema
    base_schema = Schema.query.filter_by(name='submission_base').one().json
    title = Schema.query.filter_by(name='title').one()
    subtitle = Schema.query.filter_by(name='subtitle').one()
    base_schema['properties'][title.name] = title.json
    base_schema['properties'][subtitle.name] = subtitle.json
    print(json.dumps(base_schema))

if __name__ == "__main__":
    manager.run()
