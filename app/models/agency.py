from app.database import db


class Agency(db.Model):
    """
    Define the Agency class for the table 'agency' with the following columns:
    
    ein             varchar(4), primary key
    parent_ein      varchar(3), ein of parent agency, if any
    name            varchar(256), agency name
    acronym         varchar(5), agency name acronym
    
    """
    __table_name__ = "agency"

    # columns
    ein = db.Column(db.String(4), primary_key=True)
    parent_ein = db.Column(db.String(3))
    name = db.Column(db.String(256), nullable=False)
    acronym = db.Column(db.String(10), nullable=False)

    # relationship
    registrations = db.relationship("Registration", back_populates="agency")
