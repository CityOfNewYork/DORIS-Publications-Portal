from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB
from app.database import db
from app.constants import document_action
from .event import DocumentEvent
from ._enums import user_auth_type


class Document(db.Model):
    """
    Define the Document class for the table 'publication' with the following columns:
    
    COLUMNS           MODS 3.6 EQUIVALENT      DESCRIPTION
    
    id                NA                       integer, primary key
    user_guid         NA                       varchar(64), foreign key to 'auth_user.guid'
    user_auth_type    NA                       user_auth_type, foreign key to 'auth_user.auth_type'
    title             titleInfo.title          varchar(), chief title of this resource
    subtitle          titleInfo.subTitle       varchar(), the remainder of the title information
    names             name.namePart            json, {'primary_agency': <agency_id>, 'additional_creators': [<additional_creators>]}
    type              genre.type               publication_type, ...
    date_created      originInfo.dateCreated   datetime, creation date of document record
    date_published    originInfo.dateIssued    datetime, date of publication NOT portal publication date
    language          language.languageTerm    language_code, ISO-639-2 language code
    topic             subject.topic            topic, term/phrase representing primary topic of focus
    geographic        subject.geographic       varchar(), geographic designation
    report_year_type  NA                       year_type, ENUM
    report_year_start NA                       datetime, start date
    report_year_end   NA                       datetime, end date
        
    language codes are retrieved from https://www.loc.gov/standards/iso639-2/php/code_list.php
    
    """
    __tablename__ = "document"
    __table_args__ = (
        db.ForeignKeyConstraint(
            ("user_guid", "user_auth_type"),
            ("auth_user.guid", "auth_user.auth_type")
        ),
    )
    # columns
    id = db.Column(db.Integer, primary_key=True)
    user_guid = db.Column(db.String(64), nullable=False)
    user_auth_type = db.Column(user_auth_type, nullable=False)
    title = db.Column(db.String(150), nullable=False)
    subtitle = db.Column(db.String(150))
    names = db.Column(JSONB, nullable=False)
    type = db.Column(
        db.Enum(
            "foo",
            name="document_type"
        ),
        nullable=False
    )
    date_created = db.Column(db.DateTime(), nullable=False)
    date_published = db.Column(db.DateTime(), nullable=False)
    language = db.Column(
        db.Enum(
            "bar",
            name="language"
        ),
        nullable=False
    )
    topic = db.Column(
        db.Enum(
            "baz",
            name="topic"
        ),
        nullable=False
    )
    # TODO: geographic = db.Column(db.String())
    report_year_type = db.Column(
        db.Enum(
            "quux",
            name="year_type"
        ),
        nullable=False
    )
    report_year_start = db.Column(db.DateTime(), nullable=False)
    report_year_end = db.Column(db.DateTime(), nullable=False)

    # relationships
    files = db.relationship("File", back_populates="document")
    events = db.relationship("DocumentEvent", back_populates="document", lazy="dynamic")
    submitter = db.relationship(
        "User",
        primaryjoin="and_(Document.user_guid == User.guid, "
                    "Document.user_auth_type == User.auth_type)",
        back_populates="submissions"
    )

    @property
    def status(self):
        return self.events.order_by(DocumentEvent.timestamp.desc()).first().action

    @property
    def published_date(self):
        """
        Returns the portal publication date of the document.
        :rtype: datetime
        """
        return self.events.filter_by(document_action.PUBLISHED).one().timestamp

    def as_dict(self, event_type):  # TODO: for DocumentEvent.state, possibly use DataDiff
        return {
            "title": self.title,
            "subtitle": self.subtitle,
            # ...
        }

    def __init__(self,
                 user_guid,
                 user_auth_type,
                 title,
                 names,
                 type_,
                 publisher,
                 date_published,
                 language,
                 topic,
                 temporal,
                 report_year_type,
                 report_year_start,
                 report_year_end,
                 subtitle=None
                 ):
        self.user_guid = user_guid
        self.user_auth_type = user_auth_type
        self.title = title
        self.subtitle = subtitle
        self.names = names
        self.type = type_
        self.publisher = publisher
        self.date_created = datetime.utcnow()
        self.date_published = date_published
        self.language = language
        self.topic = topic
        self.temporal = temporal
        self.report_year_type = report_year_type
        self.report_year_start = report_year_start
        self.report_year_end = report_year_end
