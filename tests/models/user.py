import unittest

from app.constants import USER_ID_DELIMETER
from app.constants.user_auth_type import NYC_EMPLOYEES
from app.database import user, registration
from tests.lib.base import BaseTestCase


class UserModelTests(BaseTestCase):

    AGENCY_EIN = "0860"
    USER_GUID = "abc123"
    USER_AUTH_TYPE = NYC_EMPLOYEES

    def setUp(self):
        super().setUp()
        self.user = user.create(self.USER_GUID, self.USER_AUTH_TYPE, "Jane", None, "Doe", "jdoe@mail.com")
        self.other_user = user.create("xyz456", self.USER_AUTH_TYPE, "John", None, "Smith", "jsmith@mail.com")

    def test_relationship_registrations(self):
        registrations = set()
        for i in range(3):
            registrations.add(registration.create(self.user.guid, self.user.auth_type, self.AGENCY_EIN))
        self.assertEqual(set(self.user.registrations.all()), registrations)

    def test_relationship_submissions(self):  # TODO
        pass

    def test_relationship_events(self):
        events = set()
        for i in range(3):
            events.add(
                registration.create_and_submit(
                    self.user.guid, self.user.auth_type, self.AGENCY_EIN
                ).events.first()  # submission event
            )
        self.assertEqual(set(self.user.events.all()), events)

    def test_get_id(self):
        self.assertEqual(self.user.get_id(), USER_ID_DELIMETER.join((self.USER_GUID, self.USER_AUTH_TYPE)))

    def test_property_registration(self):
        """ 
        The registration property of the User model must return the *latest* registration.
        """
        self.assertEqual(self.user.registration, None)
        reg = None
        for i in range(3):
            reg = registration.create_and_submit(self.user.guid, self.user.auth_type, self.AGENCY_EIN)
        self.assertEqual(self.user.registration, reg)

    def test_property_is_registered(self):
        self.assertEqual(self.user.is_registered, False)
        reg_id = registration.create_and_submit(self.user.guid, self.user.auth_type, self.AGENCY_EIN).id
        self.assertEqual(self.user.is_registered, False)
        registration.approve(reg_id, self.other_user.guid, self.other_user.auth_type)
        self.assertEqual(self.user.is_registered, True)

    def test_property_agency(self):
        """
        The agency property of the User model must return the agency associated with a
        user's registration and only if that registration has been approved.
        """
        self.assertEqual(self.user.agency, None)
        reg = registration.create_and_submit(self.user.guid, self.user.auth_type, self.AGENCY_EIN)
        self.assertEqual(self.user.agency, None)
        registration.approve(reg.id, self.other_user.guid, self.other_user.auth_type)
        self.assertEqual(self.user.agency, reg.agency)

    def test_property_name(self):
        self.assertIsInstance(self.user.name, str)


if __name__ == "__main__":
    unittest.main()
