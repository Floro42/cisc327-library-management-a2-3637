import os
from database import DATABASE, add_sample_data, init_database
import pytest
from library_service import (
    calculate_late_fee_for_book, borrow_book_by_patron, add_book_to_catalog
)

#clears the database of any previous runs of pytest so that new runs of pytest can run as expected
@pytest.fixture(autouse=True, scope="module")
def clearDatabase():
    if os.path.exists(DATABASE):
        os.remove(DATABASE)

    init_database()
    add_sample_data()
    
def test_late_fee_book_not_checked_out():
    #Tests calculating a late fee for book not borrowed by patron
    add_book_to_catalog("Test Book", "Test Author", "1234567890123", 5)
    fee_dict = calculate_late_fee_for_book("123456", 1234567890123)
    #assert fee_dict["fee_amount"] == None
    #assert fee_dict["days_overdue"] == None
    #assert "book not borrowed" in fee_dict["status"].lower()

def test_late_fee_book_valid_input():
    #Tests calculating late fee with valid input
    add_book_to_catalog("Test Book", "Test Author", "1234567890123", 5)
    borrow_book_by_patron("123456", 1234567890123)
    fee_dict = calculate_late_fee_for_book("123456", 1234567890123)
    assert fee_dict["fee_amount"] == 0.00
    assert fee_dict["days_overdue"] == 0
    assert "late fee is" in fee_dict["status"].lower()

def test_late_fee_book_invalid_book_id():
    #Tests calculating late fee with invalid book ID
    add_book_to_catalog("Test Book", "Test Author", "1234567890123", 5)
    borrow_book_by_patron("123456", 1234567890123)
    fee_dict = calculate_late_fee_for_book("123456", 1234567890123523523)
    assert fee_dict["fee_amount"] == None
    assert fee_dict["days_overdue"] == None
    assert "invalid book id" in fee_dict["status"].lower()

def test_late_fee_book_invalid_user_id():
    #Tests calculating late fee with invalid user ID
    add_book_to_catalog("Test Book", "Test Author", "1234567890123", 5)
    borrow_book_by_patron("123456", 1234567890123)
    fee_dict = calculate_late_fee_for_book("12345678", 1234567890123)
    assert fee_dict["fee_amount"] == None
    assert fee_dict["days_overdue"] == None
    assert "invalid user id" in fee_dict["status"].lower()


fee_dict = test_late_fee_book_not_checked_out()
