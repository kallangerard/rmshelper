import calc
import logging
import os
import sys
import unittest
import json

# Temporary path alteration method
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from rmshelper.rms import RMSManager
from rmshelper.secretmanager import get_secret
import rmshelper.rmshelper as rmshelper
import handler


class TestAuthentication(unittest.TestCase):
    pass


class TestRMS(unittest.TestCase):
    def setUp(self):
        self.ID = os.environ.get("TEST_ID")
        secret_name = os.environ.get("STAGE") + "/" + "rmshelper"
        region_name = os.environ.get("AWS_REGION_NAME")
        secret = json.loads(get_secret(secret_name, region_name))
        subdomain = secret.get("SUBDOMAIN")
        token = secret.get("RMS_TOKEN")
        self.order = RMSManager(subdomain, token)

    def test_rms_get_opportunity(self):
        """Test that rms.get_opportunity gives expected response
        """
        # pylint: disable=E1101
        response = self.order.get_opportunity(id=self.ID)
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


class TestRMSHelper(unittest.TestCase):
    logging.basicConfig(level=logging.INFO)

    def test_get_xero_invoice_uuid(self):
        """Tests that Xero invoice uuid can be retrieved from INV- number"""
        invoice_number = os.environ.get("TEST_XERO_INVOICE_NUMBER")
        logging.debug(f"Xero Invoice Number: {invoice_number}")
        test_invoice_uuid = os.environ.get("TEST_XERO_INVOICE_UUID")
        invoice_uuid = rmshelper.xero_order.get_invoice_uuid(invoice_number)
        self.assertEqual(invoice_uuid, test_invoice_uuid)


class TestSecretManager(unittest.TestCase):
    def test_get_secret_rms(self):
        """ Tests {stage}/rmshelper Secret Get Method for AWS
        Insert a "PING":"PONG" key:value pair into your secret
        """
        secret_name = os.environ.get("STAGE") + "/rmshelper"
        region_name = os.environ.get("AWS_REGION_NAME")
        secret = json.loads(get_secret(secret_name, region_name))
        self.assertEqual(secret.get("PING"), "PONG")

    def test_get_xero_key(self):
        """ Tests {stage}/xero Secret Key Get method for AWS"""
        secret_name = os.environ.get("STAGE") + "/xero"
        region_name = os.environ.get("AWS_REGION_NAME")
        secret = get_secret(secret_name, region_name)
        lines = secret.splitlines()
        begin_rsa = "-----BEGIN RSA PRIVATE KEY-----"
        self.assertEqual(lines[0], begin_rsa)


class TestHandler(unittest.TestCase):
    def test_quick_invoice(self):
        """Testing Quick Invoice for rmshelper"""
        # TODO: Setup and Teardown test invoice for handler.quick_invoice()
        pass


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
