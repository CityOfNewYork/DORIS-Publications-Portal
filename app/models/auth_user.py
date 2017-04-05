from flask_login import UserMixin
from app.database import db
from app.constants import user_auth_type, USER_ID_DELIMETER


class AuthUser(db.Model, UserMixin):
    """
    "auth_user"

    Most fields are provided by NYC.ID Authentication Web Service SAML Assertion.

    The combination of "guid" and "auth_type" must be unique and, thus, these
    two fields form a composite primary key.

    guid: unique identifier for the 'auth_type'
    auth_type: authentication type of user (NYC.ID or a federated identity provider)
    first_name: first name of user
    middle_initial: middle initial of user (single character)
    last_name: last name of user
    email: email address of user
    email_validated: has user has validated its email address?
    terms_of_use_accepted: has the user accepted the latest terms of use?

    """
    __tablename__ = "auth_user"
    guid = db.Column(db.String(64), primary_key=True)
    auth_type = db.Column(
        db.Enum(
            user_auth_type.NYC_ID,
            user_auth_type.NYC_EMPLOYEES,
            user_auth_type.FACEBOOK,
            user_auth_type.MICROSOFT,
            user_auth_type.YAHOO,
            user_auth_type.LINKEDIN,
            user_auth_type.GOOGLE,
            name='user_auth_type'
        ),
        primary_key=True
    )
    first_name = db.Column(db.String(32), nullable=False)
    middle_initial = db.Column(db.String(1))
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(254), nullable=False)
    email_validated = db.Column(db.Boolean(), nullable=False, default=False)
    terms_of_use_accepted = db.Column(db.Boolean(), nullable=False, default=False)

    def __init__(self,
                 guid,
                 auth_type,
                 first_name,
                 middle_initial,
                 last_name,
                 email,
                 email_validated,
                 terms_of_use_accepted):
        self.guid = guid
        self.auth_type = auth_type
        self.first_name = first_name
        self.middle_initial = middle_initial
        self.last_name = last_name
        self.email = email
        self.email_validated = email_validated
        self.terms_of_use_accepted = terms_of_use_accepted

    def get_id(self):
        return USER_ID_DELIMETER.join((self.guid, self.auth_type))
