# Library Management Web Application

A web application for a local library to manage books, members, and transactions. This project allows the librarian to track books, issue and return books, and manage rental fees with ease.

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Screenshots](#screenshots)
- [License](#license)

## Features

The Library Management System includes the following functionalities:

1. **Books Management**
    - Add new books, update book details, delete books, and manage stock.
    - Search for books by title or author.

2. **Members Management**
    - Add, update, and delete members.
    - Track member details including name, email, phone number, and rental debt.

3. **Transactions**
    - Issue books to members and record the transaction.
    - Handle book returns and charge rental fees.
    - Ensure members’ outstanding debt does not exceed KES 500 before issuing a new book.

4. **Rental Fee Management**
    - Automatically charge fees upon book return based on rental duration.

## Tech Stack

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, Bootstrap
- **Database**: SQLite (for development), Postgres/MySQL (for production)
- **Deployment**: Yet to be deployed

## Prerequisites

- **Python 3.8.10**
- **Django**
- **Virtual Environment (venv)**

## Setup

To run the project locally:

1. **Clone the repository**:
    ```bash
    git clone git@github.com:Nyae44/django-library-management.git
    cd django-library-management
    ```

2. **Ensure Python version 3.8.10**:
    Make sure you have Python 3.8.10 installed. You can check your version with:
    ```bash
    python --version
    ```
    If you don't have Python 3.8.10 installed, you can install it or use a version manager like `pyenv` to set it up.

3. **Create a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

4. **Set environment variables**:
    Create a `.env` file in the root of the project and add the following:
    ```bash
    SECRET_KEY=your-secret-key
    DEBUG=True  # Or False in production
    ```

5. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

6. **Run migrations**:
    ```bash
    python manage.py migrate
    ```

7. **Create a superuser (for the admin panel)**:
    ```bash
    python manage.py createsuperuser
    ```

8. **Run the development server**:
    ```bash
    python manage.py runserver
    ```

9. **Access the application**:
    - Go to `http://127.0.0.1:8000` in your browser to view the library management system.
    - Go to `http://127.0.0.1:8000/admin` to access the Django admin panel.

## Screenshots

### 1. Books Management

- Add, update, or delete books with stock tracking.

![Add Book](https://github.com/Nyae44/django-library-management/blob/master/screenshots/screenshot_6_add_book.png?raw=true)
![Update Book](https://github.com/Nyae44/django-library-management/blob/master/screenshots/screenshot_7_updatebook.png?raw=true)
![Delete Book](https://github.com/Nyae44/django-library-management/blob/master/screenshots/screenshot8_deletebook.png?raw=true)


### 2. Members Management

- View, add, or update member details. Track their outstanding rental debt.

![Member Management](https://github.com/Nyae44/django-library-management/blob/master/screenshots/screenshot3_members.png?raw=true)


### 3. Issuing a Book

- Issue a book to a member, with the option to manage due dates and rental fees.

![Books Management](https://github.com/Nyae44/django-library-management/blob/master/screenshots/screenshot_4_issuebook.png?raw=true)


### 4. Returning a Book & Rental Fee Calculation

- Return a book, automatically calculating and applying rental fees.

![Books Management](https://github.com/Nyae44/django-library-management/blob/master/screenshots/screenshot5_returnbook.png?raw=true)


### 5. Search for Books

- Search books by title or author.
![Books Management](https://github.com/Nyae44/django-library-management/blob/master/screenshots/screenshot9_searchbook.png?raw=true)


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
