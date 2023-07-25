import unittest
from requests import Response
import common.response_helper as response_helper

class Tests(unittest.TestCase):
    def test_get_domain_with_protocol(self):
        self.assertEqual(response_helper.get_domain("www.test.com"), "https://www.test.com")
    def test_get_fixed_url(self):
        self.assertEqual(response_helper.get_fixed_url("/test", "www.test.com"), "https://www.test.com/test")
    def test_get_redirect_from_response(self):
        resp = Response()
        resp.headers["Location"] = "/test"
        self.assertEqual(response_helper.get_redirect_from_response(resp, "www.test.com"), "https://www.test.com/test")
    def test_is_valid_url(self):
        self.assertTrue(response_helper.is_valid_url("https://www.test.com"))
    def test_is_invalid_url(self):
        self.assertFalse(response_helper.is_valid_url("test"))

if __name__ == "__main__":
    unittest.main()