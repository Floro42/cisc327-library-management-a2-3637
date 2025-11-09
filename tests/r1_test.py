import pytest

import services.library_service

from services.library_service import (
    add_book_to_catalog
)


import os
from database import init_database, add_sample_data, DATABASE

#clears the database of any previous runs of pytest so that new runs of pytest can run as expected
@pytest.fixture(autouse=True, scope="module")
def clearDatabase():
    if os.path.exists(DATABASE):
        os.remove(DATABASE)

    init_database()
    add_sample_data()

def test_add_book_valid_input():
    """Test adding a book with valid input."""
    success, message = add_book_to_catalog("Test Book", "Test Author", "1234567890123", 5)
    
    assert success == True
    assert "successfully added" in message.lower()

def test_add_book_invalid_isbn_too_short():
    """Test adding a book with ISBN too short."""
    success, message = add_book_to_catalog("Test Book", "Test Author", "123456789", 5)
    
    assert success == False
    assert "13 digits" in message

# Add more test methods for each function and edge case. You can keep all your test in a separate folder named `tests`.

def test_add_book_invalid_isbn_too_long():
    """Test adding a book with ISBN too long."""
    success, message = add_book_to_catalog("Test Book", "Test Author", "12345678236346161236139", 5)
    
    assert success == False
    assert "13 digits" in message


def test_add_book_invalid_title_too_long():
    """Test adding a book with ISBN too long."""
    success, message = add_book_to_catalog("supercalifragilisticexpialidotioussupercalifragilisticexpialidotioussupercalifragilisticexpialidotioussupercalifragilisticexpialidotioussupercalifragilisticexpialidotioussupercalifragilisticexpialidotious", "Test Author", "12345678910111213", 5)
    
    assert success == False
    assert "200 characters" in message

def test_add_book_invalid_number_of_copies_negative():
    """Test adding a book with a negative amount of copies."""
    success, message = add_book_to_catalog("Test Book", "Test Author", "1234567890123", -5)
    
    assert success == False
    assert "positive" in message

def test_add_book_invalid_author_name_too_long():
    """Test adding a book with an author name that is too long."""
    success, message = add_book_to_catalog("Test Book", "supercalifragilisticexpialidotioussupercalifragilisticexpialidotioussupercalifragilisticexpialidotious", "12345678910111213", 5)
    
    assert success == False
    assert "100 characters" in message

def main():
    test_add_book_valid_input()