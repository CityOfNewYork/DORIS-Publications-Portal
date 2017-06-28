from datetime import datetime
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from app.database import db
from app.constants import (
    language,
    document_action,
    report_year_type
)
from .report_type import ReportType
from .event import DocumentEvent
from ._enums import user_auth_type


class Document(db.Model):
    """
    Define the Document class for the table 'document' with the following columns:
    
    COLUMNS           MODS 3.6 EQUIVALENT      DESCRIPTION
    
    id                NA                       integer, primary key
    user_guid         NA                       varchar(64), foreign key to 'auth_user.guid'
    user_auth_type    NA                       user_auth_type, foreign key to 'auth_user.auth_type'
    title             titleInfo.title          varchar(), chief title of this resource
    subtitle          titleInfo.subTitle       varchar(), the remainder of the title information
    names             name.namePart            json, {'primary_agency': <agency_id>, 'additional_creators': [<additional_creators>]}
    type              genre.type               publication_type, foreign key to 'report_type.name'
    date_created      originInfo.dateCreated   datetime, creation date of document record
    date_published    originInfo.dateIssued    datetime, date of publication NOT portal publication date
    language          language.languageTerm    language_code, ISO-639-2 language code
    subject                                    array, subject(s) relevant to the report
    geographic        subject.geographic       varchar(), geographic designation
    report_year_type  NA                       year_type, ENUM
    report_year_start NA                       datetime, temporal coverage start date
    report_year_end   NA                       datetime, temporal coverage end date
        
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
    type = db.Column(db.String(64), db.ForeignKey("report_type.name"), nullable=False)
    language = db.Column(
        db.Enum(
            language.ENGLISH,
            language.SPANISH,
            language.CHINESE,
            language.RUSSIAN,
            language.ARABIC,
            language.BENGALI,
            language.FRENCH,
            language.HAITIAN_CREOLE,
            language.ITALIAN,
            language.KOREAN,
            language.POLISH,
            language.URDU,
            language.YIDDISH,
            name="language"
        ),
        nullable=False
    )
    subject = db.Column(ARRAY(db.String(120)), nullable=False)
    # TODO: geographic = db.Column(db.String())
    report_year_type = db.Column(
        db.Enum(
            report_year_type.CALENDAR,
            report_year_type.FISCAL,
            report_year_type.OTHER,
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
    def date_created(self):
        """
        Returns the date the document was created on the portal.
        :rtype: datetime
        """
        return self.events.order_by(DocumentEvent.timestamp.asc()).first().timestamp

    @property
    def date_published(self):
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
                 doc_language,
                 subject,
                 year_type,
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
        self.language = doc_language
        self.subject = subject
        self.report_year_type = year_type
        self.report_year_start = report_year_start
        self.report_year_end = report_year_end

    def __repr__(self):
        return '<Document %r>' % self.id
