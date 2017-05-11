import unittest
from app import create_app
from app.database import db, agency
from config import TST


class BaseTestCase(unittest.TestCase):
    app = create_app(TST)

    @classmethod
    def setUpClass(cls):
        with cls.app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            db.session.remove()
            db.drop_all()

    def setUp(self, populate=True):
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        if populate:
            self.populate_database()

    def tearDown(self):
        self.clear_database()
        self.app_context.pop()

    @staticmethod
    def populate_database():
        agency.populate_from_csv()

    @staticmethod
    def clear_database():
        meta = db.metadata
        # clear table contents
        for table in reversed(meta.sorted_tables):
            db.session.execute(table.delete())
        # reset sequences
        for sequence, in db.session.execute(
            "SELECT c.relname FROM pg_class c WHERE c.relkind = 'S'"
        ).fetchall():
            db.session.execute("ALTER SEQUENCE {} RESTART WITH 1;".format(sequence))
        db.session.commit()
