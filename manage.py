import os
import subprocess

from flask_migrate import Migrate, MigrateCommand, upgrade
from flask_script import Manager, Server, Shell

from config import DEV
from app import create_app
from app.database import db, user, agency, report_type

COV = None
if os.environ.get('FLASK_COVERAGE') == 'True':
    import coverage

    COV = coverage.coverage(branch=True, include='app/*', config_file=os.path.join(os.curdir, '.coveragerc'))
    COV.start()

app = create_app(DEV)
manager = Manager(app)
migrate = Migrate(app, db)


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


# deploy ---------------------------------------------------------------------------------------------------------------

@manager.command
def deploy():
    """Run deployment tasks."""
    # migrate database to the latest revision
    upgrade()

    # populate database
    agency.populate_from_csv()
    report_type.populate_from_csv()


# test -----------------------------------------------------------------------------------------------------------------

@manager.option('-t', '--test-name', help="Specify tests (file, class, or specific test)", dest='test_name')
@manager.option('-c', '--coverage', help="Run coverage analysis for tests", dest='cov')
def test(cov=False, test_name=None):
    """Run the unit tests."""
    if cov and not os.environ.get('FLASK_COVERAGE'):
        import sys
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    if not test_name:
        tests = unittest.TestLoader().discover('tests', pattern='*.py')
    else:
        tests = unittest.TestLoader().loadTestsFromName('tests.' + test_name)
    unittest.TextTestRunner(verbosity=2).run(tests)

    if COV:
        COV.stop()
        COV.save()
        print("Coverage Summary:")
        COV.report()
        COV.html_report()
        COV.xml_report()


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
manager.add_command("db", MigrateCommand)

if __name__ == "__main__":
    manager.run()
