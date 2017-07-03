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
        user.create(self.USER_GUID, self.USER_AUTH_TYPE, "Jane", None, "Doe", "jdoe@mail.com")
        self.document = document.create(self.USER_GUID,
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
                                        subtitle="Department of Records Report on Vital Records Printing"
                                        )

        # self.document_submission = document_event.create(
        #     self.USER_GUID,
        #     self.USER_AUTH_TYPE,
        #     self.document.id,
        #     document_action.SUBMITTED,
        #     self.document.as_dict
        # )

    def test_relationship_files(self):
        pass

    def test_relationship_events(self):
        pass

if __name__ == "__main__":
    unittest.main()
