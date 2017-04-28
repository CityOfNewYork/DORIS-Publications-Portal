from app.database import db
from app.constants import registration_action
from .event import RegistrationEvent
from ._enums import user_auth_type


class Registration(db.Model):
    """
    Define the Registration class for the table 'registration' with the following columns:
    
    id
    agency_ein
    registrant_guid
    registrant_auth_type    integer, primary key and foreign key to `
    
    """
    __tablename__ = "registration"
    __table_args__ = (
        db.ForeignKeyConstraint(
            ("registrant_guid", "registrant_auth_type"),
            ("auth_user.guid", "auth_user.auth_type"),
        ),
    )

    # columns
    id = db.Column(db.Integer, primary_key=True)
    registrant_guid = db.Column(db.String(64), nullable=False)
    registrant_auth_type = db.Column(user_auth_type, nullable=False)
    agency_ein = db.Column(db.String(4), db.ForeignKey("agency.ein"), nullable=False)

    # relationships
    agency = db.relationship("Agency", back_populates="registrations")
    events = db.relationship("RegistrationEvent", back_populates="registration", lazy="dynamic")
    registrant = db.relationship(
        "User",
        primaryjoin="and_(Registration.registrant_guid == User.guid, "
                    "Registration.registrant_auth_type == User.auth_type)",
        back_populates="registrations"
    )

    def __init__(self, registrant_guid, registrant_auth_type, agency_ein):
        self.registrant_guid = registrant_guid
        self.registrant_auth_type = registrant_auth_type
        self.agency_ein = agency_ein

    @property
    def status(self):
        return self.events.order_by(RegistrationEvent.timestamp.desc()).first().action

    @property
    def is_pending(self):
        return self.status == registration_action.SUBMITTED

    @property
    def is_approved(self):
        return self.status == registration_action.APPROVED

    @property
    def is_denied(self):
        return self.status == registration_action.DENIED

    @property
    def date_submitted(self):
        return self._get_date_of_action(registration_action.SUBMITTED)

    @property
    def date_approved(self):
        return self._get_date_of_action(registration_action.APPROVED)

    @property
    def date_denied(self):
        return self._get_date_of_action(registration_action.DENIED)

    def _get_date_of_action(self, action):
        return self.events.filter_by(action=action).one().timestamp
