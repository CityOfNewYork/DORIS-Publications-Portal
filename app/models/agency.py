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
    acronym = db.Column(db.String(10))

    # relationship
    registrations = db.relationship("Registration", back_populates="agency")

    def __init__(self, ein, name, acronym=None, parent_ein=None):
        self.ein = ein
        self.name = name
        self.acronym = acronym
        self.parent_ein = parent_ein

    @property
    def parent(self):
        """
        Parent agency or none.
        """
        if self.parent_ein and self.parent_ein != self.ein[1:]:
            return self.query.get("0{}".format(self.parent_ein))
