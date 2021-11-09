from sqlalchemy.orm import backref
from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    postal_code = db.Column(db.String, nullable=False)
    phone = db.Column(db.String)
    register_at = db.Column(db.DateTime)
    videos = db.relationship("Rental", backref="customer")

    def to_dict(self):
        """Converts model info into a dictionary"""
        if self.id: 
            return {
                "id": self.id,
                "name": self.name,
                "postal_code": self.postal_code,
                "phone": self.phone, 
                "register_at": self.register_at
            }