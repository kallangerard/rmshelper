import requests
import json
import os
import logging

from xero import Xero
from xero.auth import PrivateCredentials
from xero.exceptions import XeroNotFound
from datetime import datetime
from dateutil.parser import parse

from rmshelper.rms import RMSManager
from rmshelper.secretmanager import get_secret


class XeroRMS:
    def __init__(self, xero_consumer_key, xero_private_key):

        credentials = PrivateCredentials(xero_consumer_key, xero_private_key)
        self.xero = Xero(credentials)

    def get_invoice_uuid(self, invoice_number):
        # pylint: disable=E1101
        data = self.xero.invoices.filter(InvoiceNumber=invoice_number)
        logging.info(f"INVOICE OBJECT")
        logging.info(data)
        invoice_uuid = data[0]["InvoiceID"]
        return invoice_uuid

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
            print(
                f"Cleaned Invoice https://go.xero.com/AccountsReceivable/View.aspx?InvoiceID={invoice_uuid}"
            )
        # Otherwise do nothing.
        else:
            print("Invoice already clean")


def quick_invoice(opportunity_id):
    """ Function for performing a quick invoice end to end.
    Will create an invoice using the inbuilt RMS methods, post it to Xero and then clean the invoice for junk line items.
    Returns Xero Invoice uuid
    """
    rms_invoice = rms_order.post_invoice(opportunity_id)
    xero_invoice_number = rms_invoice.json()["invoice"]["number"]
    xero_invoice_uuid = xero_order.get_invoice_uuid(xero_invoice_number)
    xero_order.clean_invoice(xero_invoice_uuid)
    logging.info(
        f"Opportunity {opportunity_id} has been clean invoiced {xero_invoice_number}"
    )
    return xero_invoice_uuid


def batch_quick_invoice(*args):
    for order in args:
        try:
            quick_invoice(order)
        except:
            logging.info("Failed to process Order {order}")


def toggle_opportunity_invoiced_status(opportunity_id, override=None):
    # pylint: disable=E1101
    opportunity = rms_order.get_opportunity(opportunity_id)
    if override == None:
        x = opportunity["opportunity"]["invoiced"]
        opportunity["opportunity"]["invoiced"] = not x
    if override == True or False:
        opportunity["opportunity"]["invoiced"] = override
    # pylint: disable=E1101
    opportunity = rms_order.put_opportunity(opportunity_id, opportunity)
    return opportunity


# logging.basicConfig(level=logging.DEBUG)
region_name = os.environ.get("AWS_REGION_NAME")
logging.debug(f"Region Name: {region_name}")
xero_secret_name = os.environ.get("STAGE") + "/xero"
logging.debug(f"xero_secret_name: {xero_secret_name}")
rmshelper_secret_name = os.environ.get("STAGE") + "/rmshelper"
logging.debug(f"rmshelper_secret_name: {rmshelper_secret_name}")
rmshelper_secret = json.loads(get_secret(rmshelper_secret_name, region_name))

xero_consumer_key = rmshelper_secret.get("XERO_CONSUMER_KEY")
xero_private_key = get_secret(xero_secret_name, region_name)

rms_subdomain = rmshelper_secret.get("SUBDOMAIN")
rms_token = rmshelper_secret.get("RMS_TOKEN")

xero_order = XeroRMS(xero_consumer_key, xero_private_key)
rms_order = RMSManager(rms_subdomain, rms_token)

