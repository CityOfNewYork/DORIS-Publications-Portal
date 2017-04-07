from app.database import db

# TODO: use polymorphic relationship like in OpenRecords (timestamp, user_guid, user_auth_type)


class EventDocument(db.Model):
    """
    Define the EventDocument class for table 'event_document' with the following columns:
    
    id              integer, primary key
    type            event_doc_type, type of event for document
    timestamp       datetime, when the event occurred
    doc_id          integer, foreign key to 'document.id'
    user_guid       varchar(64), foreign key to 'auth_user.guid'
    user_auth_type  user_auth_type, foreign key to 'auth_user.auth_type'
    
    For keeping track of when a document was saved, submitted, sent back 
    for corrections, resubmitted with corrections, and approved.
        
    """
    pass


class EventRegistration(db.Model):
    """
    Define the EventRegistration class for table 'event_registration' with the following columns:
    
    id              integer, primary key
    type            event_reg_type, type of event for registration
    timestamp       datetime, when the event occurred
    reg_id          integer, foreign key to 'registration.id'
    user_guid       varchar(64), foreign key to 'auth_user.guid'
    user_auth_type  user_auth_type, foreign key to 'auth_user.auth_type'
    
    For keeping track of when a registration was created and denied and by whom.
    
    """
    pass
