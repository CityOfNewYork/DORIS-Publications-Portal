from app.database import db


class Registration(db.Model):
    """
    Define the Registration class for the table 'registration' with the following columns:
    
    registrant_guid
    registrant_auth_type
    agency_ein
    
    QUESTIONS:
    - When a user registers, agency is learned?
    - What will the supervisor field consist of?
    
    """
    pass
