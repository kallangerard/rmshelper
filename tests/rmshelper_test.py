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
    pass


class TestRMS(unittest.TestCase):
    ID = 123
    CREDENTIALS = "ABC"

    def test_rms_get(self):
        """Test that rms.get_opportunity gives expected response
        Dummy object in place for now
        """
        order = RMS()
        url = RMS.BASE_URL + "/opportunities/" + str(self.ID)
        # pylint: disable=E1101
        response = order.get_opportunity(self.CREDENTIALS, self.ID)
        logging.debug(response)
        expected_response = {"url": url, "credentials": self.CREDENTIALS}
        self.assertEqual(response, expected_response)

    def test_rms_put(self):
        """Test that rms.put_opportunity gives expected response
        Dummy object in place for now
        """
        order = RMS()
        url = RMS.BASE_URL + "/opportunities/" + str(self.ID)
        # pylint: disable=E1101
        response = order.put_opportunity(self.CREDENTIALS, self.ID)
        logging.debug(response)
        expected_response = {"url": url, "credentials": self.CREDENTIALS}
        self.assertEqual(response, expected_response)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()

