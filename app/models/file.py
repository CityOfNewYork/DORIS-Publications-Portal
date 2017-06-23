from app.database import db


class File(db.Model):
    """
    Define the File class for the table 'file' with the following columns:
    
    id              integer, primary key
    title           varchar(), user-defined title
    name            varchar(), SHA-1 hash
    hash            varchar(), the original name of the file
    document_id     integer, foreign key to 'document.id'
    
    """
    __tablename__ = "file"

    # columns
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), nullable=False)
    name = db.Column(db.String(), nullable=False)
    hash = db.Column(db.String(), nullable=False)
    document_id = db.Column(db.Integer, db.ForeignKey("document.id"), nullable=False)

    # relationships
    document = db.relationship("Document", back_populates="files")

    def __init__(self, title, name, document_id, hash_):
        self.title = title
        self.name = name
        self.document_id = document_id
        self.hash = hash_
