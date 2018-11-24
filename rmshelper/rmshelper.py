import requests
import json
import os
import logging
from secretmanager import get_secret
from xero import Xero
from xero.auth import PrivateCredentials
from xero.exceptions import XeroNotFound
from datetime import datetime
from dateutil.parser import parse


class XeroRMS:
    def __init__(self, xero_consumer_secret, xero_private_key):

        with open(xero_private_key) as keyfile:
            self.rsa_key = keyfile.read()
        credentials = PrivateCredentials(xero_consumer_secret, self.rsa_key)
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
            XeroRMS.xero.invoices.save(data)
            print("Cleaned Invoice")
        # Otherwise do nothing.
        else:
            print("Invoice already clean")

