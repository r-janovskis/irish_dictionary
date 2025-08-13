from . import db

class Word(db.Model):
    __tablename__ = "words"
    word_id = db.Column(db.Integer, primary_key = True)
    word = db.Column(db.String(100), nullable = False, unique = True)
    translation = db.Column(db.String(100), nullable = False)
    word_type = db.Column(db.Integer, db.ForeignKey("types.type_id"))

    def __repr__(self):
        return f"{self.word}: {self.translation}"
    

class Type(db.Model):
    __tablename__ = "types"
    type_id = db.Column(db.Integer, primary_key = True)
    type_name = db.Column(db.String(50), unique = True, nullable = False)

    def __repr__(self):
        return f"{self.type_id}: {self.type_name}"
    

class Category(db.Model):
    __tablename__ = "categories"
    category_id = db.Column(db.Integer, primary_key = True)
    category_name = db.Column(db.String(50), unique = True, nullable = False)

    def __repr__(self):
        return f"{self.category_id}: {self.category_name}"
    
class WordCategory(db.Model):

    __tablename__ = "word_categories"
    word_id = db.Column(db.Integer, db.ForeignKey("words.word_id"), primary_key = True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.category_id"), primary_key = True)

