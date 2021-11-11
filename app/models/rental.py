from app import db

class Rental(db.Model):
    __tablename__ = "video_rentals"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    due_date = db.Column(db.DateTime) 
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey("video.id"), nullable=False)
    customer = db.relationship("Customer", backref="rentals")
    video = db.relationship("Video", backref="rentals")

    def to_dict(self):
        if self.id: 
            available_inventory = self.video.total_inventory - len(self.video.rentals)
            videos_checked_out_count = len(self.customer.rentals)
            
            # if available_inventory < 0:
            #     remove_from_database(self)
            #     abort(400, {"message": "Could not perform checkout"})

            rental = {
                "video_id": self.video_id,
                "customer_id": self.customer_id,
                "videos_checked_out_count": videos_checked_out_count,
                "available_inventory": available_inventory
            }
        return rental