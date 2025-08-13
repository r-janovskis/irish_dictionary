import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv


load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    # Create and configure the Flask application
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    
    db.init_app(app)
    #migrate.init_app(app, db)

    # Import tables from models.py
    from .models import Word

    with app.app_context():
        db.create_all()


    
    @app.route('/', methods = ['GET'])
    def home():
        return f"Welcome to Irish Dictionary"
    
    @app.route('/words', methods = ['GET'])
    def words():
        all_words = Word.query.all()
        if not all_words:
            return jsonify({"Message": "Database is empty, no words found"}, 404)
        
        words_list = []
        for word in all_words:
            words_list.append({
                "id": word.id,
                "word": word.word,
                "translation": word.translation
            })
        return jsonify({"words": words_list}, 200)
    
    @app.route('/add_word', methods = ['POST'])
    def add_word():
        json_data = request.get_json()
        new_word = Word(word = json_data['word'], translation = json_data['translation'])

        db.session.add(new_word)
        db.session.commit()

        return jsonify({"Message": f"Word '{new_word.word}' successfully added to the database!"}, 201)
    
    
    return app

