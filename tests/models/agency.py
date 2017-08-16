import unittest

from app.constants.user_auth_type import NYC_EMPLOYEES
from app.database import user, registration
from app.database.agency import get as get_agency
from tests.lib.base import BaseTestCase


class AgencyModelTests(BaseTestCase):

    PARENT_AGENCY_EIN = "0002"
    SUB_AGENCY_EIN = "002A"

    def test_relationship_registration(self):
        agency = get_agency(self.SUB_AGENCY_EIN)
        user_auth_type = NYC_EMPLOYEES
        user_guid = "abc123" # TODO: generate_guid
        user.create(user_guid, user_auth_type,  "Jane", None, "Doe", "jdoe@mail.com")
        registration_1 = registration.create(user_guid, user_auth_type, self.SUB_AGENCY_EIN)
        registration_2 = registration.create(user_guid, user_auth_type, self.SUB_AGENCY_EIN)
        self.assertEqual(agency.registrations, [registration_1, registration_2])

    def test_property_parent(self):
        parent_agency = get_agency(self.PARENT_AGENCY_EIN)
        sub_agency = get_agency(self.SUB_AGENCY_EIN)
        self.assertEqual(parent_agency, sub_agency.parent)

    def test_property_no_parent(self):
        parent_agency = get_agency(self.PARENT_AGENCY_EIN)
        self.assertIsNone(parent_agency.parent)


if __name__ == "__main__":
    unittest.main()
