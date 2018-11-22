import calc
import logging
import os
import sys
import unittest

# # Prepend ../ to PYTHONPATH so that we can import RMSHelper from there.
# TESTS_ROOT = os.path.abspath(os.path.dirname(__file__))
# sys.path.insert(0, os.path.realpath(os.path.join(TESTS_ROOT, "..")))

from rmshelper import RMS
from rmshelper import get_secret


class TestAuthentication(unittest.TestCase):
    pass


class TestRMS(unittest.TestCase):
    ID = os.environ.get("TEST_ID")
    CREDENTIALS = os.environ.get("TEST_CREDENTIALS")
    secret_name = os.environ.get("STAGE") + "/" + "rmshelper"
    region_name = os.environ.get("AWS_REGION_NAME")
    secret = get_secret(secret_name, region_name)
    subdomain = secret.get("subdomain")
    token = secret.get("token")
    order = RMS(subdomain, token)

    def test_rms_get_opportunity(self):
        """Test that rms.get_opportunity gives expected response
        """
        url = RMS.BASE_URL + "/opportunities/" + str(self.ID)
        # pylint: disable=E1101
        response = self.order.get_opportunity(self.ID)
        logging.info(response)
        expected_response = {"url": url, "credentials": self.CREDENTIALS}
        self.assertEqual(response, expected_response)

    def test_rms_put(self):
        """Test that rms.put_opportunity gives expected response
        Dummy object in place for now
        """
        # pylint: disable=W0612
        url = RMS.BASE_URL + "/opportunities/" + str(self.ID)
        # TODO: Put test method
        pass


class TestSecretManager(unittest.TestCase):
    def test_get_secret(self):
        """ Tests Dev Secret Get Method for AWS """
        secret_name = os.environ.get("STAGE") + "/" + "rmshelper"
        region_name = os.environ.get("AWS_REGION_NAME")
        secret = get_secret(secret_name, region_name)
        self.assertEqual(secret.get("PING"), "PONG")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    unittest.main()
