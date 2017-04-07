from app.database import db
from app.models import EventDocument


class Document(db.Model):  # TODO: deal with publication.py -> document.py change
    """
    Define the Publication class for the table 'publication' with the following:
    
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
    
    QUESTIONS:
    - date issued - of original document in pdf or once published in portal?
    - Structure of name form field (just like in metadata maker)?
        structure of json?
        [
            {
                "first": "Jane"
                "last": "Doe"
                "type": "author"
                ...
            },
            ...
        ]
    - Shouldn't a table of contents be included in the PDF itself, storing it might be useless?
    - What are the contents of the type (genre.type) dropdown?
    - typeOfResource options?
    - Should topic be a user input that becomes a tag that other users can use or are we just 
        making it a dropdown?
    - Temporal options? Geographic options?
    
    """
    __tablename__ = "publication"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    subtitle = db.Column(db.String())
    names = db.Column(db.Json, nullable=False)
    type = db.Column(db.Enum(name="publication_type"), nullable=False)
    publisher = db.Column(db.varchar(), nullable=False)
    date_created = db.Column(db.datetime(), nullable=False)
    date_issued = db.Column(db.datetime(), nullable=False)
    language = db.Column(db.Enum(name="language"), nullable=False)
    topic = db.Column(db.Enum(name="topic"), nullable=False)
    geographic = db.Column(db.varchar())
    temporal = db.Column(db.Enum(name="temporal"), nullable=False)
    url = db.Column(db.varchar())

    files = db.relationship("File")
    events = db.relationship("EventDocument", lazy="dynamic")

    @property
    def status(self):  # TODO: move to registration
        return self.events.order_by(EventDocument.timestamp).first().type
