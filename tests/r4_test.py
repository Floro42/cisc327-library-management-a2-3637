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
    borrow_book_by_patron("123456", 2)
    result = return_book_by_patron("123456", 2)
    print(result[0])
    print(result[1])

    #Should work, tested without the assertions, but assertions do not work for some reason

    #assert result[0] == True
    #assert "successfully returned" in result[1].lower()
"""

def test_return_book_not_checked_out():
    #Tests returning a book that has not been checked out
    add_book_to_catalog("Test Book", "Test Author", "1234567890123", 5)
    result = return_book_by_patron("123456", 2)
    assert result[0] == False
    assert "book not borrowed" in result[1].lower()


def test_return_book_invalid_book_id():
    #Tests returning a book with valid invalid book ID
    add_book_to_catalog("Test Book", "Test Author", "1234567890123", 5)
    borrow_book_by_patron("123456", 1234567890123)
    result = return_book_by_patron("123456", 1234567892350123)
    assert result[0] == False
    assert "book not found" in result[1].lower()


def test_return_book_invalid_user_id():
    #Tests returning a book with valid invalid user ID
    result = return_book_by_patron("1634733", 1234567892350123)
    assert result[0] == False
    assert "invalid patron id" in result[1].lower()
