from app.database import db


class Agency(db.Model):
    """
    
    """
    __table_name__ = "agency"

    # columns
    ein = db.Column(db.String(4), primary_key=True)
    parent_ein = db.Column(db.String(3))
    name = db.Column(db.String(256), nullable=False)

    # relationship
    registrations = db.relationship("Registration", back_populates="agency")
