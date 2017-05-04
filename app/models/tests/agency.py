import unittest
from app.database import Agency, User, Registration
from app.tests.base import BaseTestCase
from app.constants.user_auth_type import NYC_EMPLOYEES


class AgencyModelTests(BaseTestCase):

    PARENT_AGENCY_EIN = "0002"
    SUB_AGENCY_EIN = "002A"

    def test_relationship_registration(self):
        agency = Agency.get(self.SUB_AGENCY_EIN)
        user_auth_type = NYC_EMPLOYEES
        user_guid = "abc123" # TODO: generate_guid
        User.create(user_guid, user_auth_type,  "Jane", None, "Doe", "jdoe@mail.com")
        registration_1 = Registration.create(user_guid, user_auth_type, self.SUB_AGENCY_EIN)
        registration_2 = Registration.create(user_guid, user_auth_type, self.SUB_AGENCY_EIN)
        self.assertEqual(agency.registrations, [registration_1, registration_2])

    def test_property_parent(self):
        parent_agency = Agency.get(self.PARENT_AGENCY_EIN)
        sub_agency = Agency.get(self.SUB_AGENCY_EIN)
        self.assertEqual(parent_agency, sub_agency.parent)

    def test_property_no_parent(self):
        parent_agency = Agency.get(self.PARENT_AGENCY_EIN)
        self.assertIsNone(parent_agency.parent)


if __name__ == "__main__":
    unittest.main()
