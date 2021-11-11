from app import db

class Rental(db.Model):
    __tablename__ = "video_rentals"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    due_date = db.Column(db.DateTime) 
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey("video.id"), nullable=False)
    customer = db.relationship("Customer", backref="rentals")
    video = db.relationship("Video", backref="rentals")

        