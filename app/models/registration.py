from app.database import db
from app.constants import registration_action
from .event import RegistrationEvent
from ._enums import user_auth_type


class Registration(db.Model):
    """
    Define the Registration class for the table 'registration' with the following columns:
    
    agency_ein
    registrant_guid
    registrant_auth_type
    
    QUESTIONS:
    - When a user registers, agency is learned? WELL, after user is approved, agency is saved
    - What will the supervisor field consist of?
    
    """
    registrant_guid = db.Column(db.String(64), primary_key=True)
    registrant_auth_type = db.Column(user_auth_type, primary_key=True)
    agency_ein = db.Column(db.Integer, nullable=False)

    # registrant =

    @property
    def status(self):
        return self.events.order_by(RegistrationEvent.timestamp.desc()).first().action

    @property
    def is_approved(self):
        return self.status == registration_action.APPROVED
