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
        """Retrieves the Xero invoice uuid when given an invoice number

        Parameters
        ----------
        invoice_number : string
            The invoice number of the Xero Invoice (eg "INV-1234")

        Returns
        -------
        invoice_uuid : string
            The uuid for the Xero Invoice (eg "243216c5-369e-4056-ac67-05388f86dc81")
        
        >>> invoice = XeroRMS()
        >>> invoice_uuid = invoice.get_invoice_uuid("INV-1234")
        >>> print(invoice_uuid)
        "243216c5-369e-4056-ac67-05388f86dc81"
        """

        # pylint: disable=E1101
        data = self.xero.invoices.filter(InvoiceNumber=invoice_number)
        # logging.info(f"INVOICE OBJECT")
        logging.info(data)
        invoice_uuid = data[0]["InvoiceID"]
        return invoice_uuid

    def clean_invoice(self, invoice_uuid, description_headers=None):
        """
        Will clean invoice using uuid provided and save in place a neat copy

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
            # TODO: Add method for inserting order dates and hire agreement
            self.xero.invoices.save(data)
            print(
                f"Cleaned Invoice https://go.xero.com/AccountsReceivable/View.aspx?InvoiceID={invoice_uuid}"
            )
        # Otherwise do nothing.
        else:
            print("Invoice already clean")


def batch_invoice(view_id):
    """Performs quick_invoice on a view_id of opportunities

    >>> batch_invoice(10001)
    """

    page = 1

    def _get_orders():
        """Gets list of invoiceable orders """

        # pylint: disable=E1101
        return rms_order.get_opportunities(
            params={"view_id": view_id, "per_page": 50, "page": page}
        )

    # Gets orders and filters for invoices set to automatically invoice
    # Until no more invoices remain
    while True:
        orders = _get_orders()
        filtered_orders = [
            order
            for order in orders["opportunities"]
            if order["custom_fields"]["disable_auto_invoice"] == "No"
        ]
        if len(filtered_orders) == 0:
            break
        for order in filtered_orders:
            opportunity_id = order["id"]
            if order["charge_including_tax_total"] == "0.0":
                toggle_opportunity_invoiced_status(opportunity_id, override=True)
                continue
            else:
                logging.info(f"Invoicing Opportunity {opportunity_id}")
                quick_invoice(opportunity_id)


def global_check_in(event):
    """Retreives a stock level object when given an asset_id (barcode)

    >>> global_check_in("12345")
    # TODO: Check in all booked out instances of given stock level
    """

    asset_number = event["asset_number"]
    # pylint: disable=E1101
    asset = rms_order.get_stock_levels(params={"q[asset_number_eq]": asset_number})
    print(json.dumps(asset, indent=2))


def quick_invoice(opportunity_id):
    """Function for performing a quick invoice end to end

    Will create an invoice using the inbuilt RMS methods, post it to Xero and then clean the invoice for junk line items.
    Returns dictonary of post_invoice_status_code, xero_invoice_number and xero_invoice_uuid
    """

    rms_invoice = rms_order.post_invoice(opportunity_id)
    xero_invoice_number = rms_invoice.json()["invoice"]["number"]
    xero_invoice_uuid = xero_order.get_invoice_uuid(xero_invoice_number)
    xero_order.clean_invoice(xero_invoice_uuid)
    logging.info(
        f"Opportunity {opportunity_id} has been clean invoiced {xero_invoice_number}"
    )
    return {
        "post_invoice_status_code": rms_invoice.status_code,
        "xero_invoice_number": xero_invoice_number,
        "xero_invoice_uuid": xero_invoice_uuid,
    }


def batch_quick_invoice(*args):
    """Will perform a quick invoice on any number of opportunity_id's

    >>> batch_quick_invoice(12, 13, 15)
    """

    for order in args:
        try:
            quick_invoice(order)
        except:
            logging.info("Failed to process Order {order}")


def toggle_opportunity_invoiced_status(opportunity_id, override=None):
    """Toggles the invoiced status of an opportunity

    
    >>> toggle_opportunity_invoiced_status(opportunity_id = 123)
    
    Parameters
    ----------
    opportunity_id : int
        The opportunity id
    override : boolean, optional
        Forces the status instead of toggling

    Methods
    -------
    toggle_opportunity_invoiced_status(opportunity_id, override= True)
        Forces invoiced_status to True
    toggle_opportunity_invoiced_status(opportunity_id, override= False) 
        Forces invoiced_status to False 
    """

    # pylint: disable=E1101
    opportunity = rms_order.get_opportunity(id=opportunity_id)
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
secret_name = os.environ.get("STAGE") + "/rmshelper"

secret = json.loads(get_secret(secret_name, region_name))

rms_subdomain = secret.get("SUBDOMAIN")
rms_token = secret.get("RMS_TOKEN")
r = RMSManager(rms_subdomain, rms_token)

xero_secret_name = os.environ.get("STAGE") + "/xero"
xero_consumer_key = secret.get("XERO_CONSUMER_KEY")
xero_private_key = get_secret(xero_secret_name, region_name)
x = XeroRMS(xero_consumer_key, xero_private_key)

