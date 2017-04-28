from app.database import db
from app.constants import document_action
from .event import DocumentEvent
from ._enums import user_auth_type


class Document(db.Model):
    """
    Define the Document class for the table 'publication' with the following columns:
    
    COLUMNS         MODS 3.6 EQUIVALENT     DESCRIPTION
    
    id              NA                      integer, primary key
    title           titleInfo.title         varchar(), chief title of this resource
    subtitle        titleInfo.subTitle      varchar(), the remainder of the title information
    names           name.namePart           json, ...
    type            genre.type              publication_type, ...
    publisher       originInfo.publisher    varchar(), entity that produced this resource
    date_created    originInfo.dateCreated  datetime, date of creation
    date_issued     originInfo.dateIssuesd  datetime, date of publication
    language        language.languageTerm   language_code, ISO-639-2 language code
    topic           subject.topic           topic, term/phrase representing primary topic of focus
    geographic      subject.geographic      varchar(), geographic designation
    temporal        subject.temporal        temporal, chronological subject terms or temporal coverage
    url             location.url            varchar(), Uniform Resource Location of resource
                                                       (once available on portal)
    submitter_guid                          varchar(64), foreign key to 'auth_user.guid'
    submitter_auth_type                     user_auth_type, foreign key to 'auth_user.auth_type'
        
    language codes are retrieved from https://www.loc.gov/standards/iso639-2/php/code_list.php
    
    """
    __tablename__ = "document"
    __table_args__ = (
        db.ForeignKeyConstraint(
            ("submitter_guid", "submitter_auth_type"),
            ("auth_user.guid", "auth_user.auth_type")
        ),
    )
    # columns
    id = db.Column(db.Integer, primary_key=True)
    submitter_guid = db.Column(db.String(64), nullable=False)
    submitter_auth_type = db.Column(user_auth_type, nullable=False)
    title = db.Column(db.String(), nullable=False)
    subtitle = db.Column(db.String())
    names = db.Column(db.JSON(), nullable=False)
    type = db.Column(
        db.Enum(
            "foo",
            name="document_type"
        ),
        nullable=False
    )
    publisher = db.Column(db.String(), nullable=False)
    date_created = db.Column(db.DateTime(), nullable=False)
    date_issued = db.Column(db.DateTime(), nullable=False)
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
    geographic = db.Column(db.String())
    temporal = db.Column(
        db.Enum(
            "qux",
            name="temporal"
        ),
        nullable=False
    )
    url = db.Column(db.String())

    # relationships
    files = db.relationship("File", back_populates="document")
    events = db.relationship("DocumentEvent", back_populates="document", lazy="dynamic")
    submitter = db.relationship(
        "User",
        primaryjoin="and_(Document.submitter_guid == User.guid, "
                    "Document.submitter_auth_type == User.auth_type)",
        back_populates="submissions"
    )

    @property
    def status(self):
        return self.events.order_by(DocumentEvent.timestamp.desc()).first().action

    @property
    def date_created(self):
        return self.events.order_by(DocumentEvent.timestamp.asc()).first().timestamp

    @property
    def date_published(self):
        return self.events.filter_by(document_action.PUBLISHED).one().timestamp

    def as_dict(self, event_type):  # TODO: for DocumentEvent.state, possibly use DataDiff
        return {
            "title": self.title,
            "subtitle": self.subtitle,
            # ...
        }
