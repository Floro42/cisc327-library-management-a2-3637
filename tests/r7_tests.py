import pytest
from library_service import(
    add_book_to_catalog, borrow_book_by_patron, get_patron_status_report
)

"""
def test_valid_input_patron_status():
    add_book_to_catalog("Test Book", "Test Author", "1234567890123", 5)
    borrow_book_by_patron("123456", 1234567890123) 
    results = get_patron_status_report("123456")
    #assuming currently borrowed links to a dictionary connecting the book id with the title
    assert results["currently borrowed"][1234567890123] == "Test Book"
    assert results["fees"] == 0
    assert results["books borrowed"] == 1 
    assert results["browsing record"] != None


def test_patron_id_too_short():
    results = get_patron_status_report("12345")
    assert results == False


def test_patron_id_too_long():
    results = get_patron_status_report("1234567")
    assert results == False


def test_patron_status_no_books_borrowed():
    results = get_patron_status_report("123456")
    assert results["currently borrowed"] == False
"""