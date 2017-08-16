import unittest
from datetime import datetime

from dateutil.relativedelta import relativedelta

from app.constants import document_action
from app.constants.user_auth_type import NYC_EMPLOYEES
from app.database import document, document_event, user
from tests.lib.base import BaseTestCase


class DocumentModelTests(BaseTestCase):
    USER_GUID = "abc123"
    USER_AUTH_TYPE = NYC_EMPLOYEES

    def setUp(self):
        super().setUp()
        # TODO: create User and Document factories
        user.create(self.USER_GUID, self.USER_AUTH_TYPE, "Jane", None, "Doe", "jdoe@mail.com")
        document_args = (
            self.USER_GUID,
            self.USER_AUTH_TYPE,
            "Annual Report",
            {
                "primary_agency": "0860",
                "additional_creators": ["0858", "Thomas Foley"]
            },
            "reports_annual",
            "english",
            ["politics_government", "civil_service"],
            "calendar",
            datetime.now() - relativedelta(years=1),
            datetime.now(),
            document_action.SUBMITTED,
        )

        self.document = document.create(*document_args,
                                        subtitle="Report on Vital Records Printing")

        self.event_args = (
            self.USER_GUID,
            self.USER_AUTH_TYPE,
            self.document.id
        )

    def test_relationship_files(self):
        # TODO
        pass

    def test_relationship_events(self):
        event_1 = document_event.create(*(self.event_args + (document_action.SAVED,)))
        event_2 = document_event.create(*(self.event_args + (document_action.CHANGES_REQUESTED,)))
        self.assertEqual(self.document.events.all(), [event_1, event_2])

    def test_relationship_submitter(self):
        submitter = user.get(self.USER_GUID, self.USER_AUTH_TYPE)
        self.assertEqual(self.document.submitter, submitter)

if __name__ == "__main__":
    unittest.main()
