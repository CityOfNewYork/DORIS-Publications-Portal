from sqlalchemy import desc
from flask_login import UserMixin
from app.database import db
from app.constants import USER_ID_DELIMETER
from ._enums import user_auth_type as enum_user_auth_type


class User(db.Model, UserMixin):
    """
    Define the User class for table 'auth_user' with the following columns:

    guid                    varchar(64), unique identifier for the 'auth_type'
    auth_type               user_auth_type, authentication type of user (NYC.ID or a federated identity provider)
    first_name              varchar(64), first name of user
    middle_initial          varchar(1), middle initial of user (single character)
    last_name               varchar(64), last name of user
    email                   varchar(254), email address of user
    phone                   varchar(25), phone number of variable format
    email_validated         boolean, has user has validated its email address?
    terms_of_use_accepted   boolean, has the user accepted the latest terms of use?
    agency_ein              varchar(3), foreign key to 'agency' table
    is_poc                  boolean, is the user an agency point of contact?
    is_admin                boolean, is the user an administrator (member of DORIS library staff)?
    is_super                boolean, is the user an all-powerful super user?

    Most fields are provided by NYC.ID Authentication Web Service SAML Assertion.

    The combination of "guid" and "auth_type" must be unique and therefore 
    is used as a primary composite key.
    
    """
    __tablename__ = "auth_user"

    # columns
    guid = db.Column(db.String(64), primary_key=True)
    auth_type = db.Column(enum_user_auth_type, primary_key=True)  # FIXME: not needed since only agency users can login
    first_name = db.Column(db.String(64), nullable=False)
    middle_initial = db.Column(db.String(1))
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(254), nullable=False, unique=True)
    phone = db.Column(db.String(25))
    email_validated = db.Column(db.Boolean(), nullable=False, default=False)
    terms_of_use_accepted = db.Column(db.Boolean(), nullable=False, default=False)
    is_poc = db.Column(db.Boolean(), nullable=False, default=False)
    is_admin = db.Column(db.Boolean(), nullable=False, default=False)
    is_super = db.Column(db.Boolean(), nullable=False, default=False)

    # relationships
    registrations = db.relationship(
        "Registration",
        primaryjoin="and_(User.guid == Registration.user_guid, "
                    "User.auth_type == Registration.user_auth_type)",
        back_populates="registrant",
        lazy="dynamic"
    )
    submissions = db.relationship(
        "Document",
        primaryjoin="and_(User.guid == Document.user_guid, "
                    "User.auth_type == Document.user_auth_type)",
        back_populates="submitter",
        lazy="dynamic"
    )
    events = db.relationship(
        "_Event",
        primaryjoin="and_(User.guid == _Event.user_guid, "
                    "User.auth_type == _Event.user_auth_type)",
        back_populates="agent",
        lazy="dynamic"
    )

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

    def __repr__(self):
        return '<User "{}" ({}, {})>'.format(self.name, self.guid, self.auth_type, self.name)

    def get_id(self):
        """
        Overrides UserMixin.get_id()
        """
        return USER_ID_DELIMETER.join((self.guid, self.auth_type))

    @property
    def registration(self):
        """
        A user's latest registration, if any.
        """
        return self.registrations.join("events").order_by(desc("timestamp")).first()

    @property
    def is_registered(self):
        """
        Is the user's latest registration, if any, approved?
        """
        return self.registration.is_approved if self.registration is not None else False

    @property
    def agency(self):
        """ 
        A user's agency is determined by its latest approved registration, if any.
        """
        if self.is_registered:
            return self.registration.agency

    @property
    def name(self):
        if self.middle_initial is not None:
            name = "{f} {m}. {l}".format(f=self.first_name.title(),
                                         m=self.middle_initial.upper(),
                                         l=self.last_name.title())
        else:
            name = " ".join((self.first_name.title(), self.last_name.title()))
        return name
