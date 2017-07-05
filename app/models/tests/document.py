import unittest
from datetime import datetime
from dateutil.relativedelta import relativedelta
from app.database import document, document_event, user
from app.tests.base import BaseTestCase
from app.constants import document_action
from app.constants.user_auth_type import NYC_EMPLOYEES


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
        )

        self.document = document.create(*document_args,
                                        subtitle="Report on Vital Records Printing")

        self.event_args = (
            self.USER_GUID,
            self.USER_AUTH_TYPE,
            self.document.id
        )

        args = (self.USER_GUID, self.USER_AUTH_TYPE)

        # created document
        self.created_document = document.create(*document_args)
        self.created_document_submission = document_event.create(
            *(args + (self.created_document.id, document_action.SUBMITTED, self.created_document.as_dict())))

        # published document
        self.published_document = document.create(*document_args)
        self.published_document_submission = document_event.create(
            *(args + (self.published_document.id, document_action.PUBLISHED, self.published_document.as_dict())))

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

    def test_property_status(self):
        self.assertEqual(self.created_document.status, document_action.SUBMITTED)
        self.assertEqual(self.published_document.status, document_action.PUBLISHED)

    def test_property_date_created(self):
        self.assertEqual(self.created_document_submission.timestamp, self.created_document.date_created)

    def test_property_date_published(self):
        self.assertEqual(self.published_document_submission.timestamp, self.published_document.date_published)

if __name__ == "__main__":
    unittest.main()
