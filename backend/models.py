from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


#TODO Figure out
class Songs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    song_name = db.Column(db.String(255), nullable=False)
    artist = db.Column(db.String(255), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    processed_json = db.Column(db.JSON, nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
