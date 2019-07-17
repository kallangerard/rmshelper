import json
import logging
import os
from datetime import datetime

import requests
from dateutil.parser import parse
from oauthlib.oauth1 import SIGNATURE_HMAC, SIGNATURE_RSA, SIGNATURE_TYPE_AUTH_HEADER
from requests_oauthlib import OAuth1
from xero import Xero
from xero.auth import PrivateCredentials
from xero.exceptions import XeroNotFound

from .rms import RMSManager
from .secretmanager import get_secret


class XeroRMS:
    def __init__(self, xero_consumer_key, xero_private_key):

        self.credentials = PrivateCredentials(xero_consumer_key, xero_private_key)
        self.xero = Xero(self.credentials)

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

    def email_invoice(self, xero_invoice_uuid):
        oauth = OAuth1(
            self.credentials.consumer_key,
            resource_owner_key=self.credentials.oauth_token,
            rsa_key=self.credentials.rsa_key,
            signature_method=SIGNATURE_RSA,
            signature_type=SIGNATURE_TYPE_AUTH_HEADER,
        )
        post_url = (
            f"https://api.xero.com/api.xro/2.0/Invoices/{xero_invoice_uuid}/Email"
        )
        session = requests.Session()
        session.auth = oauth
        return session.post(post_url)

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


def global_check_in(event, r):
    """Retreives a stock level object when given an asset_id (barcode)

    >>> global_check_in("12345")
    # TODO: Check in all booked out instances of given stock level
    """

    # asset_number = event["asset_number"]
    # pylint: disable=E1101
    # asset = r.get_stock_levels(params={"q[asset_number_eq]": asset_number})


def quick_invoice(opportunity_id, r, x):
    """Function for performing a quick invoice end to end

    Will create an invoice using the inbuilt RMS methods, post it to Xero and then clean the invoice for junk line items.
    Returns dictonary of post_invoice_status_code, xero_invoice_number and xero_invoice_uuid
    """

    rms_invoice = r.post_invoice(opportunity_id)
    xero_invoice_number = rms_invoice.json()["invoice"]["number"]
    xero_invoice_uuid = x.get_invoice_uuid(xero_invoice_number)
    x.clean_invoice(xero_invoice_uuid)
    logging.info(
        f"Opportunity {opportunity_id} has been clean invoiced {xero_invoice_number}"
    )
    return {
        "post_invoice_status_code": rms_invoice.status_code,
        "xero_invoice_number": xero_invoice_number,
        "xero_invoice_uuid": xero_invoice_uuid,
    }


def void_invoice(opportunity_id, r, x):
    # Current API Does not allow listing invoices for opportunity!
    # Get invoices for opportunity
    # For those invoices, void each one
    # Return statuses
    #         "opportunity_id": opportunity_id,
    #         "invoice_number": invoice["xero_invoice_number"],
    #         "invoice_status": invoice["invoice_status"]
    #         "status_code": invoice["post_invoice_status_code"],
    pass


def toggle_opportunity_invoiced_status(opportunity_id, r, x, override=None):
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
    opportunity = r.get_opportunity(id=opportunity_id)
    if override == None:
        x = opportunity["opportunity"]["invoiced"]
        opportunity["opportunity"]["invoiced"] = not x
    if override == True or False:
        opportunity["opportunity"]["invoiced"] = override
    # pylint: disable=E1101
    opportunity = r.put_opportunity(opportunity_id, opportunity)
    return opportunity
