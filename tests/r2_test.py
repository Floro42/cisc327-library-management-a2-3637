import pytest
from typing import Dict, List
from database import (
    get_all_books
)

import os
from database import init_database, add_sample_data, DATABASE

#clears the database of any previous runs of pytest so that new runs of pytest can run as expected
if os.path.exists(DATABASE):
    os.remove(DATABASE)

init_database()
add_sample_data()

def test_returns_correct_type():
    assert isinstance(get_all_books(), List)



def test_list_is_of_dicts():
    bookList = get_all_books()
    for book in bookList:
        assert isinstance(book, Dict)




def test_returns_empty_list():
    if os.path.exists(DATABASE):
        os.remove(DATABASE)

    init_database()

    #Empty List
    assert get_all_books() == []
