import unittest
from unittest.mock import patch
from backend.webscraper import scrape_and_find_sequences
from backend.lotto_database import create_connection, create_tables, save_sequences_to_db

class TestWebScraper(unittest.TestCase):
    
    def test_scrape_and_save_to_db(self):
        # Scraping actual web page content
        url = 'https://megalotto.pl/wyniki/lotto/losowania-z-roku-2024'
        sequences = scrape_and_find_sequences(url)
        
        # Creating connection to database
        conn = create_connection('lotto.db')
        cursor = conn.cursor()
        
        # Fetching sequences from database
        cursor.execute('SELECT * FROM lotto_results')
        rows = cursor.fetchall()
        
        # Convert rows to list of strings
        rows_as_strings = [list(map(str, row)) for row in rows]
        
        # Removing 'id' from database rows
        rows_without_id = [row[1:] for row in rows_as_strings]
        
        # Asserting that sequences from web scraping match sequences from database
        self.assertEqual(sequences, rows_without_id)

class TestCreateTables(unittest.TestCase):

    @patch('backend.lotto_database.create_connection')
    def test_create_tables(self, mock_create_connection):
        # Mocking database connection
        mock_conn = mock_create_connection.return_value
        mock_cursor = mock_conn.cursor.return_value

        # Execute function to create tables
        create_tables(mock_conn, 'Lotto')
        create_tables(mock_conn, 'EuroJackpot')
        create_tables(mock_conn, 'MiniLotto')

        # Check if create_tables method was called with correct parameters
        mock_cursor.execute.assert_any_call('CREATE TABLE IF NOT EXISTS lotto_results\n                     (id INTEGER PRIMARY KEY AUTOINCREMENT, \n                     number1 INTEGER, \n                     number2 INTEGER, \n                     number3 INTEGER, \n                     number4 INTEGER, \n                     number5 INTEGER, \n                     number6 INTEGER)')
        mock_cursor.execute.assert_any_call('CREATE TABLE IF NOT EXISTS eurojackpot_results\n                     (id INTEGER PRIMARY KEY AUTOINCREMENT, \n                     number1 INTEGER, \n                     number2 INTEGER, \n                     number3 INTEGER, \n                     number4 INTEGER, \n                     number5 INTEGER)')
        mock_cursor.execute.assert_any_call('CREATE TABLE IF NOT EXISTS minilotto_results\n                     (id INTEGER PRIMARY KEY AUTOINCREMENT, \n                     number1 INTEGER, \n                     number2 INTEGER, \n                     number3 INTEGER, \n                     number4 INTEGER, \n                     number5 INTEGER)')

if __name__ == '__main__':
    unittest.main()
