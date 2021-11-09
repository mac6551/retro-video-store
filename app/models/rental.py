from sqlalchemy.orm import backref
from app import db

class Rental(db.Model):
    __tablename__ = "video_rentals"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    due_date = db.Column(db.DateTime) 
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), primary_key=True, nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey("video.id"), primary_key=True, nullable=False)
    Customer = db.relationship("Customer", back_populates="video")
    video = db.relationship("Video", back_populates="customer")