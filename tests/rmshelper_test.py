import calc
import logging
import os
import sys
import unittest


# Prepend ../ to PYTHONPATH so that we can import RMSHelper from there.
TESTS_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.realpath(os.path.join(TESTS_ROOT, "..")))

from rmshelper import RMS
from rmshelper import get_secret


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
        logging.info(response)
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
        logging.info(response)
        expected_response = {"url": url, "credentials": self.CREDENTIALS}
        self.assertEqual(response, expected_response)


class TestSecretManager(unittest.TestCase):
    def test_get_secret(self):
        """ Tests Dev Secret Get Method for AWS """

        region_name = "ap-southeast-2"
        secret_name = "dev/rmshelper"
        secret = get_secret(secret_name, region_name)
        self.assertEqual(secret.get("RMS_API_TOKEN"), "TESTDATA_RMS_API_TOKEN")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    unittest.main()

