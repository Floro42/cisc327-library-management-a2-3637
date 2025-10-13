import pytest
import sys

from library_service import (
    borrow_book_by_patron, add_book_to_catalog
)

import os
from database import init_database, add_sample_data, DATABASE, insert_book

#clears the database of any previous runs of pytest so that new runs of pytest can run as expected
@pytest.fixture(autouse=True, scope="module")
def clearDatabase():
    if os.path.exists(DATABASE):
        os.remove(DATABASE)

    init_database()
    add_sample_data()

def test_borrow_book_valid_input():
    #Test borrowing a book with valid input.
    success, message = borrow_book_by_patron("123456", 2) 
    
    print(message)

    assert success == True
    assert "successfully borrowed" in message.lower()




def test_borrow_book_low_id_digits():
    """Test using a patron id with too few digits"""
    success, message = borrow_book_by_patron("12345", 1234567890123) 
    
    assert success == False
    assert "6 digits" in message


def test_borrow_book_high_id_digits():
    """Test using a patron id with too many digits"""
    success, message = borrow_book_by_patron("1234567", 1234567890123) 
    
    assert success == False
    assert "6 digits" in message


def test_borrow_book_negative_book_id():
    """Test using a negative book ID"""
    success, message = borrow_book_by_patron("123456", -1234567890123) 
    
    assert success == False
    assert "not found" in message


def test_borrow_book_no_copies():
    """Test using a book with no copies"""
    add_book_to_catalog("Test Book", "Test Author", "1234567890123", 0)
    success, message = borrow_book_by_patron("123456", 1234567890123) 
    
    assert success == False
    assert "not found" in message

