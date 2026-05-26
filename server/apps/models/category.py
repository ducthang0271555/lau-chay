from apps.extensions import db

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    # Liên kết với Product
    products = db.relationship('Product', backref='category', lazy=True)