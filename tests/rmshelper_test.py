import calc
import logging
import os
import sys
import unittest


# Prepend ../ to PYTHONPATH so that we can import RMSHelper from there.
TESTS_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.realpath(os.path.join(TESTS_ROOT, "..")))

from rmshelper import RMS


class TestAuthentication(unittest.TestCase):
    def test_rms_get(self):
        id = 123
        credentials = "ABC"
        rms = RMS()
        url = RMS.BASE_URL + "/opportunities/" + str(id)
        response = rms.get_opportunity(credentials, id)
        expected_response = {"url": url, "credentials": credentials}
        self.assertEqual(response, expected_response)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()

