import unittest
from flask import Flask, jsonify, request
from app import create_app, db
from app.models import Book
import json

class BookRoutesTestCase(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Setup for all tests"""
        cls.app = create_app()
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'  # Use existing database for tests
        cls.app.config['TESTING'] = True
        with cls.app.app_context():
            db.create_all()  # Ensure tables are created (if not already in the existing database)

    @classmethod
    def tearDownClass(cls):
        """Teardown for all tests - delete data after tests"""
        with cls.app.app_context():
            # Delete all data from the Book table
            Book.query.delete()  # This clears all rows from the Book table.
            db.session.commit()  # Commit the transaction to ensure data is deleted
            db.session.remove()  # Close the session

    def setUp(self):
        """Setup for individual tests"""
        self.client = self.app.test_client()

    def tearDown(self):
        """Teardown for individual tests"""
        pass

    # Test index route
    def test_index(self):
        """Test that the index route returns the correct message"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "hello from the backend")

    # Test creating a new book
    def test_create_book(self):
        """Test creating a book"""
        book_data = {
            "title": "The Catcher in the Rye",
            "author": "J.D. Salinger",
            "genre": "Fiction",
            "year_published": 1951
        }
        response = self.client.post('/books', json=book_data)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn("Book created", data['message'])
        self.assertEqual(data['book']['title'], "The Catcher in the Rye")

    # Test getting a book by title (valid title)
    def test_get_book_by_title(self):
        """Test getting a book by title"""
        book_data = {
            "title": "To Kill a Mockingbird",
            "author": "Harper Lee",
            "genre": "Fiction",
            "year_published": 1960
        }
        
        self.client.post('/books', json=book_data)
        response = self.client.get('/books/title?title=To Kill a Mockingbird')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(data), 0)
        self.assertEqual(data[0]['title'], "To Kill a Mockingbird")

    # Test getting a book by title (non-existent title)
    def test_get_non_existent_book(self):
        """Test getting a non-existent book by title"""
        response = self.client.get('/books/title?title=Nonexistent Book')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['error'], "Book not found")

    # Test getting all books
    def test_get_all_books(self):
        """Test getting all books"""
        book_data1 = {
            "title": "1984",
            "author": "George Orwell",
            "genre": "Dystopian",
            "year_published": 1949
        }
        book_data2 = {
            "title": "Brave New World",
            "author": "Aldous Huxley",
            "genre": "Dystopian",
            "year_published": 1932
        }
        self.client.post('/books', json=book_data1)
        self.client.post('/books', json=book_data2)
        response = self.client.get('/books')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(data), 0)

if __name__ == '__main__':
    unittest.main()
