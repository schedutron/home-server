from globalimports import db

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(64), index=True, unique=True)
    likes = db.Column(db.Integer, index=True, default=0)
