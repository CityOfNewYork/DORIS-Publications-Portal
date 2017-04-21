from datetime import datetime
from app.database import db
from ._enums import user_auth_type
from app.constants import document_action, registration_action


class _Event(db.Model):
    """
    Define the Event class for table 'event' with the following columns:
    
    id              integer, primary key
    timestamp       datetime, when the event occurred
    user_guid       varchar(64), foreign key to 'auth_user.guid'
    user_auth_type  user_auth_type, foreign key to 'auth_user.auth_type'
    
    """
    __tablename__ = "event"
    __mapper_args__ = {'polymorphic_on': type}

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    user_guid = db.Column(db.Column(64), nullable=False)
    user_auth_type = db.Column(user_auth_type, nullable=False)
    type = db.Column(
        db.Enum(
            "document",
            "registration",
            name="event_type"
        ),
        nullable=False
    )

    def __init__(self, user_guid, user_auth_type):
        self.user_guid = user_guid
        self.user_auth_type = user_auth_type
        self.timestamp = datetime.utcnow()


class DocumentEvent(_Event):
    """
    Define the EventDocument class for table 'event_document' with the following columns:
    
    id              integer, foreign key to `event.id`
    document_id     integer, foreign key to 'document.id'
    action          document_action, the action that was performed on the document
    state           JSON, state of document corresponding to the action
    
    """
    __tablename__ = "event_document"
    __mapper_args__ = {'polymorphic_identity': "document"}

    # columns
    id = db.Column(db.Integer, db.ForeignKey(_Event.id), primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey("document.id"), nullable=False)
    action = db.Column(db.Enum(*document_action.ALL, name="document_action"), nullable=False)
    state = db.Column(db.JSON())

    # relationships
    document = db.relationship("Document", back_populates="events")

    def __init__(self, user_guid, user_auth_type, state=None):
        super().__init__(user_guid, user_auth_type)
        self.state = state


class RegistrationEvent(_Event):
    """
    Define the EventRegistration class for table 'event_registration' with the following columns:
    
    id                  integer, foreign key to `event.id`
    registration_id     integer, foreign key to 'document.id'
    action              registration_action, the action that was performed on the registration
    
    """
    __tablename__ = "event_registration"
    __mapper_args__ = {'polymorphic_identity': "registration"}
    __table_args__ = [
        db.UniqueConstraint("registration_id", "action")  # only one of each action per registration
    ]

    # columns
    id = db.Column(db.Integer, db.ForeignKey(_Event.id), primary_key=True)
    registration_id = db.Column(db.Integer, db.ForeignKey("registration.id"), nullable=False)
    action = db.Column(db.Enum(*registration_action.ALL, name="document_action"), nullable=False)

    # relationships
    registration = db.relationship("Registration", back_populates="events")
