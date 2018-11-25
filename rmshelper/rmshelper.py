import requests
import json
import os
import logging

from xero import Xero
from xero.auth import PrivateCredentials
from xero.exceptions import XeroNotFound
from datetime import datetime
from dateutil.parser import parse

from .rms import RMSManager
from .secretmanager import get_secret


class XeroRMS:
    def __init__(self, xero_consumer_secret, xero_private_key):

        credentials = PrivateCredentials(xero_consumer_secret, xero_private_key)
        self.xero = Xero(credentials)

    def get_invoice_uuid(self, invoice_number):
        # pylint: disable=E1101
        data = self.xero.invoices.filter(InvoiceNumber=invoice_number)
        return data[0]["InvoiceID"]

    def clean_invoice(self, invoice_uuid):
        """
        Will clean invoice using uuid provided and save in place a neat copy.
        Removes any items that do not have a UnitAmount or UnitAmount == 0
        """
        # pylint: disable=E1101
        data = self.xero.invoices.get(invoice_uuid)
        line_items = data[0]["LineItems"]
        cleaned_items = list(
            filter(lambda x: x.get("UnitAmount", None) != 0.0, line_items)
        )

        # If filtered items are different to original items.
        if data[0]["LineItems"] != cleaned_items:
            remove_fields = ("TaxType", "TaxAmount", "LineAmount")
            # Removes fields from Line Items to allow saving/PUT
            for i in cleaned_items:
                for ii in remove_fields:
                    i.pop(ii, None)
            data[0]["LineItems"] = cleaned_items
            self.xero.invoices.save(data)
            print("Cleaned Invoice")
        # Otherwise do nothing.
        else:
            print("Invoice already clean")


def quick_invoice(opportunity_id):
    """ Function for performing a quick invoice end to end.
    Will create an invoice using the inbuilt RMS methods, post it to Xero and then clean the invoice for junk line items.
    """
    rms_invoice = rms_order.post_invoice(opportunity_id)
    xero_invoice_number = rms_invoice["invoice"]["id"]
    xero_invoice_uuid = xero_order.get_invoice_uuid(xero_invoice_number)
    xero_order.clean_invoice(xero_invoice_uuid)


def batch_quick_invoice(*args):
    for order in args:
        try:
            quick_invoice(order)
        except:
            logging.info("Failed to process Order {order}")


region_name = os.environ.get("AWS_REGION_NAME")
xero_secret_name = os.environ.get("STAGE") + "/xero"
rmshelper_secret_name = os.environ.get("STAGE") + "/rmshelper"
rmshelper_secret = json.loads(get_secret(rmshelper_secret_name, region_name))

xero_consumer_secret = rmshelper_secret.get("XERO_CONSUMER_SECRET")
xero_private_key = get_secret(xero_secret_name, region_name)

rms_subdomain = rmshelper_secret.get("RMS_SUBDOMAIN")
rms_token = rmshelper_secret.get("RMS_TOKEN")

xero_order = XeroRMS(xero_consumer_secret, xero_private_key)
rms_order = RMSManager(rms_subdomain, rms_token)


def main():
    logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    main()
