from flask import request, jsonify
from .models import db, Book

def register_routes(app):
    @app.route('/', methods=["GET"])
    def index():
        return "hello from the backend"
    # Create a new book
    @app.route('/books', methods=['POST'])
    def create_book():
        data = request.json
        book = Book(**data)
        db.session.add(book)
        db.session.commit()
        return jsonify({"message": "Book created", "book": data, "id": book.id}), 201

    # Get a single book by title using query parameters
    @app.route('/books/title', methods=['GET'])
    def get_book_by_title():
        title = request.args.get('title') 
        if not title:
            return jsonify({"error": "Title parameter is required"}), 400

        book = Book.query.filter_by(title=title).first()
        if book:
            return jsonify({
                "id": book.id,
                "title": book.title,
                "author": book.author,
                "genre": book.genre, 
                "year_published": book.year_published
            }), 200
        return jsonify({"error": "Book not found"}), 404

    # Get all books
    @app.route('/books', methods=['GET'])
    def get_all_books():
        books = Book.query.all()
        result = [
            {
                "id": book.id,
                "title": book.title,
                "author": book.author,
                "genre": book.genre,
                "year_published": book.year_published
            }
            for book in books
        ]
        return jsonify(result),  200
