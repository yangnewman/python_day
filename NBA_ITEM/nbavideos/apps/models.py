from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Nba(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50),  nullable=False)
    image = db.Column(db.String(150), nullable=False)
    time = db.Column(db.String(50), nullable=True)
    url = db.Column(db.String(150), unique=True, nullable=True)

    __tablename__ = 'nba'