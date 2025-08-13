from . import db

class Word(db.Model):
    __tablename__ = "words"
    id = db.Column(db.Integer, primary_key = True)
    word = db.Column(db.String(100), nullable = False, unique = True)
    translation = db.Column(db.String(100), nullable = False)

    def __repr__(self):
        return f"{self.word}: {self.translation}"