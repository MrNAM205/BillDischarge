# packages/backend/models.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bill_number = db.Column(db.String(255))
    amount = db.Column(db.Float)

    def __repr__(self):
        return f'<Bill {self.bill_number}>'