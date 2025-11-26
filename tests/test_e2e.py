import pytest
from playwright.sync_api import sync_playwright, Playwright, expect

def test_add_book_borrow_book():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto('http://localhost:5000')

        page.get_by_text('Add Book').click();

        #Assert that we can see the header of the Add New Book page to varify we're in the right page
        expect(page.get_by_text('Add a new book to the library catalog')).to_be_visible()

        #Fills out the book info and adds it to catalog
        page.get_by_label('Title').fill('One Piece')
        page.get_by_label('Author').fill('Eiichiro Oda')
        page.get_by_label('ISBN').fill('1111111111111')
        page.get_by_label('Total Copies').fill('12')
        page.get_by_text('Add Book to Catalog').click()

        #Assert that the adding of the book was successful
        expect(page.get_by_text('successfully added to the catalog')).to_be_visible()
        expect(page.get_by_role('cell', name ='One Piece')).to_be_visible()
        expect(page.get_by_role('cell', name ='Eiichiro Oda')).to_be_visible()
        expect(page.get_by_text('/12 Available')).to_be_visible()

        #Note, the database must be reset between tests to work properly
        #Gets the Patron ID fill box for the added book
        page.get_by_role('row', name = '4 One Piece Eiichiro Oda').get_by_placeholder('Patron ID (6 digits)').click()

        #Enters Patron ID
        page.get_by_role('row', name = '4 One Piece Eiichiro Oda').get_by_placeholder('Patron ID (6 digits)').fill('123456')

        #Borrows the book
        page.get_by_role('cell', name = '123456 Borrow').get_by_role('button').click()

        #Verifies the book was successfully borrowed and the proper amount was borrowed
        expect(page.get_by_text('Successfully borrowed')).to_be_visible()
        expect(page.get_by_text('11/12')).to_be_visible()



def test_return_book():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto('http://localhost:5000')
        page.get_by_role('row', name = '1 The Great Gatsby	F. Scott Fitzgerald').get_by_placeholder('Patron ID (6 digits)').click()

        #Enters Patron ID
        page.get_by_role('row', name = '1 The Great Gatsby	F. Scott Fitzgerald').get_by_placeholder('Patron ID (6 digits)').fill('123456')

        #Borrows the book
        page.get_by_role('cell', name = '123456 Borrow' ).get_by_role('button').click()

        #Verifies the book was successfully borrowed and the proper amount was borrowed
        expect(page.get_by_text('Successfully borrowed')).to_be_visible()

        # Click the return book link
        page.get_by_text('Return Book').click()
        expect(page.get_by_text('Return a borrowed book to the library.')).to_be_visible()
        page.get_by_label('Patron ID').fill('123456')
        page.get_by_label('Book ID').fill('1')

        page.get_by_text('Process Return').click()

        expect(page.get_by_text('Book successfully returned.')).to_be_visible()