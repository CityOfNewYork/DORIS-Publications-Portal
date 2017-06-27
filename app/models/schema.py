from sqlalchemy.dialects.postgresql import JSONB
from app.database import db


class Schema(db.Model):
    __tablename__ = "schema"
    # columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    json = db.Column(JSONB, nullable=False)
