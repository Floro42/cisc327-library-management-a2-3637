import pytest
from library_service import (
    search_books_in_catalog, add_book_to_catalog
)

def test_valid_search_partial_matching_title():
    """Tests that the partial matching aspect of searching titles works properly"""
    add_book_to_catalog("abcdefghijklmnop", "Test Author", "1234567890123", 5)
    results = search_books_in_catalog("abcdef", "partial")
    #assumption of how the keys work linking numbers of most relevant searches to best matching titles
    assert results[0].lower() == "abcdefghijklmnop"


def test_valid_search_partial_matching_author():
    """Tests that the partial matching aspect of searching authors works properly"""
    add_book_to_catalog("abcdefghijklmnop", "Test Author", "1234567890123", 5)
    results = search_books_in_catalog("test", "partial")
    #assumption of how the keys work linking numbers of most relevant searches to best matching titles
    assert results[0].lower() == "abcdefghijklmnop"


def test_valid_search_exact_matching_isbn():
    """Tests that the exact matching aspect of searching isbn works properly"""
    add_book_to_catalog("abcdefghijklmnop", "Test Author", "1234567890123", 5)
    results = search_books_in_catalog("1234567890123", "exact")
    #assumption of how the keys work linking numbers of most relevant searches to best matching titles
    assert results[0].lower() == "abcdefghijklmnop"


def test_search_no_results():
    """Tests that the function generates properly input when there are no matching results"""
    results = search_books_in_catalog("1234567890123", "exact")
    #checking to see if the dictionary of results is empty
    assert results == False