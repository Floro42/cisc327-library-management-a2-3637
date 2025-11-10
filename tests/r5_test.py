import datetime
import os
from database import DATABASE, add_sample_data, init_database
import pytest

from unittest.mock import (
    Mock, patch
)

from services.library_service import (
    calculate_late_fee_for_book, borrow_book_by_patron, add_book_to_catalog
)

#clears the database of any previous runs of pytest so that new runs of pytest can run as expected
@pytest.fixture(autouse=True, scope="module")
def clearDatabase():
    if os.path.exists(DATABASE):
        os.remove(DATABASE)

    init_database()
    add_sample_data()
    
"""
def test_late_fee_book_not_checked_out():
    #Tests calculating a late fee for book not borrowed by patron
    add_book_to_catalog("Test Book", "Test Author", "1234567890123", 5)
    fee_dict = calculate_late_fee_for_book("123456", 1234567890123)
    assert fee_dict["fee_amount"] == None
    assert fee_dict["days_overdue"] == None
    assert "book not borrowed" in fee_dict["status"].lower()
"""
    

def test_late_fee_book_valid_input(mocker):
    #Tests calculating late fee with valid input

    tweaking = [
        {'book_id': 5, 'borrow_date': datetime.date(2025,8,9)}, 
        {'book_id': 2, 'borrow_date': datetime.date(2025,8,9)}
        ]

    mocker.patch("database.get_patron_borrowed_books", return_value = tweaking)

    fee_dict = calculate_late_fee_for_book("654321", 5)
    assert fee_dict["fee_amount"] == 0.00
    assert fee_dict["days_overdue"] == 0
    assert "late fee is" in fee_dict["status"].lower()




"""def test_late_fee_book_invalid_book_id(mocker):
    #Tests calculating late fee with invalid book ID

    mocker.patch("database.get_patron_borrowed_books", return_value = [{'book_id': 4}, {'book_id': 2}])

    fee_dict = calculate_late_fee_for_book("123456", 1234567890123523523)
    assert fee_dict["fee_amount"] == 0.0
    assert fee_dict["days_overdue"] == 0
    assert "not borrowed" in fee_dict["status"].lower()"""

def test_late_fee_book_invalid_user_id():
    #Tests calculating late fee with invalid user ID

    borrow_book_by_patron("1234567", 1234567890123)
    fee_dict = calculate_late_fee_for_book("apples", 1234567890123)
    assert fee_dict["fee_amount"] == 0
    assert fee_dict["days_overdue"] == 0
    assert "invalid" in fee_dict["status"].lower()

