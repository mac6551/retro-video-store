from app import db

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(db.DateTime)
    total_inventory = db.Column(db.Integer)

    def to_dict(self):
        """Converts model info into a dictionary"""
        if self.id:
            video = {
                "id": self.id,
                "title": self.title,
                "release_date": self.release_date,
                "total_inventory": self.total_inventory 
            }
        return video