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
    from .models import Word, Type, Category, WordCategory

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

            # Get categories for the word
            categories = WordCategory.query.filter_by(word_id = word.word_id).all()
            category_names = []
            for category in categories:
                category_name = Category.query.filter_by(category_id = category.category_id).first().category_name
                category_names.append(category_name)
            # Get the type name for the word
            type = Type.query.filter_by(type_id = word.word_type).first().type_name
            

            words_list.append({
                "id": word.word_id,
                "word": word.word,
                "translation": word.translation,
                "category": category_names,
                "type": type
            })
        return jsonify({"words": words_list}, 200)
    
    @app.route('/add_word', methods = ['POST'])
    def add_word():
        json_data = request.get_json()

        # Extract information from request and create a new Word instance
        type_id = Type.query.filter_by(type_name = json_data['type']).first().type_id
        new_word = Word(word = json_data['word'], translation = json_data['translation'], word_type = type_id)

        # Commit the new word
        db.session.add(new_word)
        db.session.commit()

        # Extract WordCategory information
        category_id = Category.query.filter_by(category_name = json_data['category']).first().category_id
        new_word_category = WordCategory(word_id = new_word.word_id, category_id = category_id)
        
        db.session.add(new_word_category)
        db.session.commit()

        return jsonify({"Message": f"Word '{new_word.word}' successfully added to the database!"}, 201)
    
    @app.route('/add_type', methods = ['POST'])
    def add_type():
        json_data = request.get_json()
        new_type = Type(type_name = json_data['type_name'])

        db.session.add(new_type)
        db.session.commit()

        return jsonify({'Message': f"New type '{json_data['type_name']}' successfully added!"}, 201)
    

    @app.route('/add_category', methods = ['POST'])
    def add_category():
        json_data = request.get_json()
        new_category = Category(category_name = json_data['category_name'])

        db.session.add(new_category)
        db.session.commit()

        return jsonify({'Message': f"New type '{json_data['category_name']}' successfully added!"}, 201)



    return app

