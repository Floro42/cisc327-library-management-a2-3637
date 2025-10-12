from database import DATABASE, add_sample_data, init_database
import pytest
from library_service import (
    return_book_by_patron, borrow_book_by_patron, add_book_to_catalog
)

import os
#clears the database of any previous runs of pytest so that new runs of pytest can run as expected
@pytest.fixture(autouse=True, scope="module")
def clearDatabase():
    if os.path.exists(DATABASE):
        os.remove(DATABASE)

    init_database()
    add_sample_data()

"""
def test_return_book_valid_input():
    #Tests returning a book with valid input
    add_book_to_catalog("Test Book", "Test Author", "1234567890123", 5)
    borrow_book_by_patron("123456", 1234567890123)
    success, message = return_book_by_patron("123456", 1234567890123)
    assert success == True
    assert "successfully returned" in message.lower()


def test_return_book_not_checked_out():
    #Tests returning a book that has not been checked out
    add_book_to_catalog("Test Book", "Test Author", "1234567890123", 5)
    success, message = return_book_by_patron("123456", 1234567890123)
    assert success == False
    assert "book not checked out" in message.lower()


def test_return_book_invalid_book_id():
    #Tests returning a book with valid invalid book ID
    add_book_to_catalog("Test Book", "Test Author", "1234567890123", 5)
    borrow_book_by_patron("123456", 1234567890123)
    success, message = return_book_by_patron("123456", 1234567892350123)
    assert success == False
    assert "invalid book id" in message.lower()


def test_return_book_invalid_user_id():
    #Tests returning a book with valid invalid user ID
    success, message = return_book_by_patron("1634733", 1234567892350123)
    assert success == False
    assert "invalid book id" in message.lower()
"""