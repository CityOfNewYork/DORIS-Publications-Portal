from app import db


class ReportType(db.Model):
    """
    Define the class ReportType for the table 'report_type' with the following columns:

    id      integer, primary key
    name    varchar(64), a report type
    """
    __tablename__ = "report_type"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)

    def __repr__(self):
        return '<Report Type %r>' % self.name
