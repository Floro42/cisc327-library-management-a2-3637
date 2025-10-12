import pytest
import os

from library_service import (
    add_book_to_catalog
)

from database import init_database, add_sample_data, DATABASE

#clears the database of any previous runs of pytest so that new runs of pytest can run as expected
if os.path.exists(DATABASE):
    os.remove(DATABASE)

init_database()
add_sample_data()

def test_add_book_valid_input():
    """Test adding a book with valid input."""
    success, message = add_book_to_catalog("Test Book", "Test Author", "1234567890123", 5)
    
    assert success == True
    assert "successfully added" in message

def test_add_book_invalid_isbn_too_short():
    """Test adding a book with ISBN too short."""
    success, message = add_book_to_catalog("Test Book", "Test Author", "123456789", 5)
    
    assert success == False
    assert "13 digits" in message


# Add more test methods for each function and edge case. You can keep all your test in a separate folder named `tests`.

def main():
    test_add_book_valid_input()