from apps.extensions import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    passcode = db.Column(db.String(6), unique=True, nullable=False)
    role = db.Column(db.Integer, default=0) # 0: Nhân viên, 1: Admin
    is_active = db.Column(db.Boolean, default=True)