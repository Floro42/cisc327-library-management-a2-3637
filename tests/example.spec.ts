import { test, expect } from '@playwright/test';

test('add book and borrow book', async ({ page }) => {
  await page.goto('http://localhost:5000');

  await page.getByText('Add Book').click();

  //Assert that we can see the header of the Add New Book page to varify we're in the right page
  await expect(page.getByText('Add a new book to the library catalog')).toBeVisible();

  //Fills out the book info and adds it to catalog
  await page.getByLabel('Title').fill('One Piece');
  await page.getByLabel('Author').fill('Eiichiro Oda');
  await page.getByLabel('ISBN').fill('1111111111111');
  await page.getByLabel('Total Copies').fill('12');
  await page.getByText('Add Book to Catalog').click();

  //Assert that the adding of the book was successful
  await expect(page.getByText('successfully added to the catalog')).toBeVisible();
  await expect(page.getByRole('cell', { name: 'One Piece' })).toBeVisible();
  await expect(page.getByRole('cell', { name: 'Eiichiro Oda' })).toBeVisible();
  await expect(page.getByText('/12 Available')).toBeVisible();

  //Note, the database must be reset between tests to work properly
  //Gets the Patron ID fill box for the added book
  await page.getByRole('row', { name: '4 One Piece Eiichiro Oda' }).getByPlaceholder('Patron ID (6 digits)').click();

  //Enters Patron ID
  await page.getByRole('row', { name: '4 One Piece Eiichiro Oda' }).getByPlaceholder('Patron ID (6 digits)').fill('123456');

  //Borrows the book
  await page.getByRole('cell', { name: '123456 Borrow' }).getByRole('button').click();

  //Verifies the book was successfully borrowed and the proper amount was borrowed
  await expect(page.getByText('Successfully borrowed')).toBeVisible();
  await expect(page.getByText('11/12')).toBeVisible();
});

//Runs after the first test runs
test('return book', async ({ page }) => {
  await page.goto('http://localhost:5000');


  await page.getByRole('row', { name: '1 The Great Gatsby	F. Scott Fitzgerald' }).getByPlaceholder('Patron ID (6 digits)').click();

  //Enters Patron ID
  await page.getByRole('row', { name: '1 The Great Gatsby	F. Scott Fitzgerald' }).getByPlaceholder('Patron ID (6 digits)').fill('123456');

  //Borrows the book
  await page.getByRole('cell', { name: '123456 Borrow' }).getByRole('button').click();

  //Verifies the book was successfully borrowed and the proper amount was borrowed
  await expect(page.getByText('Successfully borrowed')).toBeVisible();

  // Click the return book link
  await page.getByText('Return Book').click();
  await expect(page.getByText('Return a borrowed book to the library.')).toBeVisible();
  await page.getByLabel('Patron ID').fill('123456');
  await page.getByLabel('Book ID').fill('1');

  await page.getByText('Process Return').click();

  await expect(page.getByText('Book successfully returned.')).toBeVisible();

});
