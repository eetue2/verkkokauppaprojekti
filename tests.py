import csv
import unittest
from unittest.mock import patch
from products import lisays

class TestMainFunctions(unittest.TestCase):

    def tearDown(self):
        # Remove the product added during the test from tuotteet.csv
        with open("tuotteet.csv", 'r') as file:
            products = [row['product'] for row in csv.DictReader(file)]

        # Find the product added during the test
        test_product = "TestProduct"  # Replace with the actual product name used in the test
        if test_product in products:
            with open("tuotteet.csv", 'w', newline='') as file:
                fieldnames = ['product', 'price', 'product_id']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()

    @patch('builtins.input', side_effect=['TestProduct', '20.0'])
    def test_lisays_success(self, mock_input):
        result = lisays(mock_input())
        self.assertTrue(result, "lisays function should return True for a successful product addition")

    @patch('builtins.input', side_effect=['TestProduct', 'invalid_price'])
    def test_lisays_invalid_price(self, mock_input):
        with self.assertRaises(ValueError, msg="lisays function should raise ValueError for an invalid price"):
            lisays(mock_input())

if __name__ == '__main__':
    unittest.main()
