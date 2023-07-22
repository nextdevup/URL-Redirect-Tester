import unittest
import common.response_helper as response_helper

class TestIOHelper(unittest.TestCase):
    def test_is_valid_url(self):
        self.assertTrue(response_helper.is_valid_url("https://www.google.com"))

if __name__ == "__main__":
    unittest.main()