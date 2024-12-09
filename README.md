### Library Management System
This is a simple Library Management System built with Flask and SQLAlchemy. It allows for CRUD operations (Create, Read, Update, Delete) on books in a library. The application supports fetching books by their title, creating new books, and managing them via RESTful APIs.

1. How to Run the Project
Prerequisites
Python 3.6+ installed on your system.
Pip for installing dependencies.
A terminal or command prompt.
Installation Steps
Clone the repository:

```bash
git clone https://github.com/yourusername/library-management-system.git
```

Create a virtual environment and Activate the virtual environment On Windows:
```bash
python3 -m venv venv
.\venv\Scripts\activate
```
On macOS/Linux:
```bash
source venv/bin/activate
```

Install the required dependencies:
```bash
   pip install -r requirements.txt
```

Run the Flask development server:
```bash
   flask run
```
This will start the server at http://127.0.0.1:5000/ by default. You can use Postman or any API testing tool to interact with the API.

## Runing the test cases 

```bash
   python -m unittest discover tests
```

