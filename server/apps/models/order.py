from apps.extensions import db
from datetime import datetime


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    table_id = db.Column(db.Integer, db.ForeignKey('tables.id'), nullable=False)
    total_amount = db.Column(db.Float, default=0.0)
    payment_method = db.Column(db.String(20))  # Cash, Transfer
    status = db.Column(db.Integer, default=0)  # 0: Chờ, 1: Đã thanh toán
    created_at = db.Column(db.DateTime, default=datetime.now)

    items = db.relationship('OrderItem', backref='order', lazy=True)