import calc
import logging
import os
import sys
import unittest
import json

# Temporary path alteration method
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from rmshelper import rms
from rmshelper import secretmanager


class TestAuthentication(unittest.TestCase):
    pass


class TestRMS(unittest.TestCase):
    def setUp(self):
        self.ID = os.environ.get("TEST_ID")
        secret_name = os.environ.get("STAGE") + "/" + "rmshelper"
        region_name = os.environ.get("AWS_REGION_NAME")
        secret = json.loads(secretmanager.get_secret(secret_name, region_name))
        subdomain = secret.get("SUBDOMAIN")
        token = secret.get("RMS_TOKEN")
        self.order = rms.RMS(subdomain, token)

    def test_rms_get_opportunity(self):
        """Test that rms.get_opportunity gives expected response
        """
        # pylint: disable=E1101
        response = self.order.get_opportunity(self.ID)
        opportunity_number = response["opportunity"]["number"]
        logging.info(json.dumps(response, indent=2))
        expected_response = os.environ.get("RMS_TEST_OPPORTUNITY_NUMBER")
        self.assertEqual(opportunity_number, expected_response)

    def test_rms_put(self):
        """Test that rms.put_opportunity gives expected response
        Dummy object in place for now
        """
        # TODO: Put test method
        pass


class TestSecretManager(unittest.TestCase):
    def test_get_secret_rms(self):
        """ Tests {stage}/rmshelper Secret Get Method for AWS
        Insert a "PING":"PONG" key:value pair into your secret
        """
        secret_name = os.environ.get("STAGE") + "/" + "rmshelper"
        region_name = os.environ.get("AWS_REGION_NAME")
        secret = json.loads(secretmanager.get_secret(secret_name, region_name))
        self.assertEqual(secret.get("PING"), "PONG")

    def test_get_xero_key(self):
        """ Tests {stage}/xero Secret Key Get method for AWS"""
        secret_name = os.environ.get("STAGE") + "/" + "xero"
        region_name = os.environ.get("AWS_REGION_NAME")
        secret = secretmanager.get_secret(secret_name, region_name)
        lines = secret.splitlines()
        begin_rsa = "-----BEGIN RSA PRIVATE KEY-----"
        self.assertEqual(lines[0], begin_rsa)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # unittest.main()
