from app.database import db
from app.constants import registration_action
from .event import RegistrationEvent
from ._enums import user_auth_type


class Registration(db.Model):
    """
    Define the Registration class for the table 'registration' with the following columns:
    
    agency_ein
    registrant_guid
    registrant_auth_type    integer, primary key and foreign key to `
    
    The combination of values of these 3 columns must be unique.
    
    """
    __tablename__ = "registration"

    # columns
    registrant_guid = db.Column(db.String(64), primary_key=True)
    registrant_auth_type = db.Column(user_auth_type, primary_key=True)
    agency_ein = db.Column(db.Integer, db.ForeignKey("agency.ein"), primary_key=True)

    __table_args__ = (
        db.ForeignKeyConstraint(
            [registrant_guid, registrant_auth_type],
            ["user.guid", "user.auth_type"],
            onupdate="CASCADE"
        ),
    )

    # relationships
    agency = db.relationship("Agency", back_populates="registrations")
    registrant = db.relationship("User", back_populates="registration")
    events = db.relationship("RegistrationEvent", back_populates="registration")

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
