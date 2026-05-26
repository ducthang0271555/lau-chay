from apps.extensions import db

class Table(db.Model):
    __tablename__ = 'tables'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    status = db.Column(db.Integer, default=0) # empty, occupied