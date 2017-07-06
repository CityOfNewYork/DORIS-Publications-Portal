from datetime import datetime
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from app.database import db
from app.constants import (
    language,
    document_action,
    report_year_type
)
from .report_type import ReportType
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
    date_created      NA                       datetime, date the document was created on the portal
    date_published    NA                       datetime, portal publication date
    report_year_type  NA                       year_type, ENUM
    report_year_start NA                       datetime, temporal coverage start date
    report_year_end   NA                       datetime, temporal coverage end date
    status            NA                       document_action, ENUM

    language codes are retrieved from https://www.loc.gov/standards/iso639-2/php/code_list.php
    
    """
    __tablename__ = "document"
    __table_args__ = (
        db.ForeignKeyConstraint(
            ("user_guid", "user_auth_type"),
            ("auth_user.guid", "auth_user.auth_type")
        ),
        db.UniqueConstraint("id", "report_type"),
    )
    # columns
    id = db.Column(db.Integer, primary_key=True)
    user_guid = db.Column(db.String(64), nullable=False)
    user_auth_type = db.Column(user_auth_type, nullable=False)
    title = db.Column(db.String(150), nullable=False)
    subtitle = db.Column(db.String(150))
    names = db.Column(JSONB, nullable=False)
    report_type = db.Column(db.String(64), db.ForeignKey("report_type.value"), nullable=False)
    language = db.Column(
        db.Enum(*tuple([l.value for l in list(language.ALL)]), name="language"),
        nullable=False
    )
    subjects = db.Column(ARRAY(db.String(120)), nullable=False)
    # TODO: geographic = db.Column(db.String())
    date_created = db.Column(db.DateTime(), nullable=False)
    date_published = db.Column(db.DateTime())
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
    status = db.Column(db.Enum(*document_action.ALL, name="document_action"), nullable=False)

    # relationships
    files = db.relationship("File", back_populates="document")
    events = db.relationship("DocumentEvent", back_populates="document", lazy="dynamic")
    submitter = db.relationship(
        "User",
        primaryjoin="and_(Document.user_guid == User.guid, "
                    "Document.user_auth_type == User.auth_type)",
        back_populates="submissions"
    )

    def as_dict(self):  # TODO: for DocumentEvent.state, possibly use DataDiff
        return {
            "title": self.title,
            "subtitle": self.subtitle,
            "names": self.names,
            "report_type": self.report_type,
            "language": self.language,
            "subjects": self.subjects,
            "report_year_type": self.report_year_type,
            "report_year_start": self.report_year_start.isoformat(),
            "report_year_end": self.report_year_end.isoformat()
        }

    def __init__(self,
                 user_guid,
                 user_auth_type,
                 title,
                 names,
                 type_,
                 doc_language,
                 subjects,
                 year_type,
                 report_year_start,
                 report_year_end,
                 status,
                 subtitle=None,
                 date_published=None
                 ):
        self.user_guid = user_guid
        self.user_auth_type = user_auth_type
        self.title = title
        self.subtitle = subtitle
        self.names = names
        self.report_type = type_
        self.language = doc_language
        self.subjects = subjects
        self.date_created = datetime.utcnow()
        self.date_published = date_published
        self.report_year_type = year_type
        self.report_year_start = report_year_start
        self.report_year_end = report_year_end
        self.status = status

    def __repr__(self):
        return '<Document %r>' % self.id
