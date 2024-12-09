from flask import request, jsonify
from .models import db, Book

def register_routes(app):
    #index route
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

    # Get books by title using query parameters
    @app.route('/books/title', methods=['GET'])
    def get_book_by_title():
        title = request.args.get('title')
        if not title:
            return jsonify({"error": "Title parameter is required"}), 400

        books = Book.query.filter(Book.title.ilike(f'%{title}%')).all()
        if books:
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
            return jsonify(result), 200

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

    # Update a book (PUT)
    @app.route('/books', methods=['PUT'])
    def update_book():
        book_id = request.args.get('id')  # Get book id from query parameters
        if not book_id:
            return jsonify({"error": "ID parameter is required"}), 400

        book = Book.query.get(book_id)
        if not book:
            return jsonify({"error": "Book not found"}), 404

        data = request.json
        book.title = data.get("title", book.title)
        book.author = data.get("author", book.author)
        book.genre = data.get("genre", book.genre)
        book.year_published = data.get("year_published", book.year_published)

        db.session.commit()
        return jsonify({
            "message": "Book updated",
            "book": {
                "id": book.id,
                "title": book.title,
                "author": book.author,
                "genre": book.genre,
                "year_published": book.year_published
            }
        }), 200

    # Delete a book (DELETE)
    @app.route('/books', methods=['DELETE'])
    def delete_book():
        book_id = request.args.get('id')  # Get book id from query parameters
        if not book_id:
            return jsonify({"error": "ID parameter is required"}), 400

        book = Book.query.get(book_id)
        if not book:
            return jsonify({"error": "Book not found"}), 404

        db.session.delete(book)
        db.session.commit()
        return jsonify({"message": "Book deleted"}), 200
