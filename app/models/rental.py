from sqlalchemy.orm import backref
from app import db

class Rental(db.Model):
    __tablename__ = "video_rentals"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    due_date = db.Column(db.DateTime) 
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey("video.id"), nullable=False)
    customer = db.relationship("Customer", backref="rentals")
    video = db.relationship("Video", backref="rentals")

    # refactor into one to dict?
    def check_out_to_dict(self): 
        if self.id:
            return {
                "customer_id": self.customer_id,
                "video_id": self.video_id,
                "due_date": self.due_date,
                "videos_checked_out_count": len(self.Customer.video),
                "available_inventory": self.video.total_inventory
            }

    def check_in_to_dict(self): 
        if self.id:
            return {
                "customer_id": self.customer_id,
                "video_id": self.video_id,
                "videos_checked_out_count": len(self.Customer.video),
                "available_inventory": self.video.total_inventory
            }
        