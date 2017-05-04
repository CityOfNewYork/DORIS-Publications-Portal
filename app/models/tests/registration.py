import unittest
from app.constants import registration_action
from app.database import Registration, Agency, User, RegistrationEvent
from app.tests.base import BaseTestCase
from app.constants.user_auth_type import NYC_EMPLOYEES
from sqlalchemy.exc import SQLAlchemyError


class RegistrationModelTests(BaseTestCase):

    AGENCY_EIN = "0860"
    USER_GUID = "abc123"
    USER_AUTH_TYPE = NYC_EMPLOYEES

    def setUp(self):
        super().setUp()
        User.create(self.USER_GUID, self.USER_AUTH_TYPE, "Jane", None, "Doe", "jdoe@mail.com")
        registration_args = (
            self.USER_GUID,
            self.USER_AUTH_TYPE,
            self.AGENCY_EIN
        )
        self.registration = Registration.create(*registration_args)
        self.event_args = (
            self.USER_GUID,
            self.USER_AUTH_TYPE,
            self.registration.id,
        )

        args = (self.USER_GUID, self.USER_AUTH_TYPE)

        # approved registration
        self.approved_registration = Registration.create(*registration_args)
        self.approved_registration_submission = RegistrationEvent.create(
            *(args + (self.approved_registration.id, registration_action.SUBMITTED)))
        self.approved_registration_approval = RegistrationEvent.create(
            *(args + (self.approved_registration.id, registration_action.APPROVED)))

        # denied registration
        self.denied_registration = Registration.create(*registration_args)
        self.denied_registration_submission = RegistrationEvent.create(
            *(args + (self.denied_registration.id, registration_action.SUBMITTED)))
        self.denied_registration_denial = RegistrationEvent.create(
            *(args + (self.denied_registration.id, registration_action.DENIED)))

    def test_relationship_agency(self):
        agency = Agency.get(self.AGENCY_EIN)
        self.assertEqual(self.registration.agency, agency)

    def test_relationship_events(self):
        event_1 = RegistrationEvent.create(*(self.event_args + (registration_action.APPROVED,)))
        event_2 = RegistrationEvent.create(*(self.event_args + (registration_action.DENIED,)))
        self.assertEqual(self.registration.events.all(), [event_1, event_2])

    def test_relationship_registrant(self):
        registrant = User.get(self.USER_GUID, self.USER_AUTH_TYPE)
        self.assertEqual(self.registration.registrant, registrant)

    def test_property_is_pending(self):
        RegistrationEvent.create(*(self.event_args + (registration_action.SUBMITTED,)))
        self.assertTrue(self.registration.is_pending)
        self.assertFalse(any((self.registration.is_approved, self.registration.is_denied)))

    def test_property_is_approved(self):
        self.assertTrue(self.approved_registration.is_approved)
        self.assertFalse(any((self.approved_registration.is_pending, self.approved_registration.is_denied)))

    def test_property_is_denied(self):
        self.assertTrue(self.denied_registration.is_denied)
        self.assertFalse(any((self.denied_registration.is_approved, self.denied_registration.is_pending)))

    def test_property_date_submitted(self):
        self.assertEqual(self.denied_registration_submission.timestamp, self.denied_registration.date_submitted)
        self.assertEqual(self.approved_registration_submission.timestamp, self.approved_registration.date_submitted)

    def test_property_date_approved(self):
        self.assertEqual(self.approved_registration_approval.timestamp, self.approved_registration.date_approved)
        self.assertEqual(self.approved_registration.date_denied, None)

    def test_property_date_denied(self):
        self.assertEqual(self.denied_registration_denial.timestamp, self.denied_registration.date_denied)
        self.assertEqual(self.denied_registration.date_approved, None)

    def test_unique_constraint(self):
        args = (self.event_args + (registration_action.APPROVED,))
        RegistrationEvent.create(*args)
        with self.assertRaises(SQLAlchemyError):
            RegistrationEvent.create(*args)


if __name__ == "__main__":
    unittest.main()
