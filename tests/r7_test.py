from database import DATABASE, add_sample_data, init_database
import pytest
from services.library_service import(
    add_book_to_catalog, borrow_book_by_patron, get_patron_status_report
)

import os
#clears the database of any previous runs of pytest so that new runs of pytest can run as expected
@pytest.fixture(autouse=True, scope="module")
def clearDatabase():
    if os.path.exists(DATABASE):
        os.remove(DATABASE)

    init_database()
    add_sample_data()


def test_valid_input_patron_status():
    results = get_patron_status_report("123456")
    #assuming currently borrowed links to a dictionary connecting the book id with the title
    assert results["currentlyBorrowedBooks"][0]['book_id'] == 3
    assert results["totalLateFees"] > 0
    assert results["numberOfCurrentlyBorrowedBooks"] == 1 
    assert results["borrowingHistory"] != None


def test_patron_id_too_short():
    results = get_patron_status_report("12345")
    assert "invalid patron" in results["error"].lower()


def test_patron_id_too_long():
    results = get_patron_status_report("1234567")
    assert "invalid patron" in results["error"].lower()


def test_patron_status_no_books_borrowed():
    results = get_patron_status_report("567890")
    assert results["currentlyBorrowedBooks"] == []
