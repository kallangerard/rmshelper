import os
import sys
import logging
import json
from datetime import datetime

from rmshelper import rmshelper


def quick_invoice(event, context=None):
    invoice = rmshelper.quick_invoice(event["opportunity_id"], r, x)
    if invoice["post_invoice_status_code"] == 200:
        return {"statusCode": 200, "body": invoice}
    # TODO: Raise exceptions

stage = os.environ.get("STAGE")

# Get RMS Secret
region_name = os.environ.get("AWS_DEFAULT_REGION")
secret_name = f"{stage}/rmshelper"
rmshelper_secret = json.loads(
    rmshelper.get_secret(secret_name, region_name)
)

#Create RMS Object
rms_subdomain = rmshelper_secret.get("SUBDOMAIN")
rms_token = rmshelper_secret.get("RMS_TOKEN")
r = rmshelper.RMSManager(rms_subdomain, rms_token)

#Create Xero Object
xero_secret_name = f"{stage}/xero"
xero_consumer_key = rmshelper_secret.get("XERO_CONSUMER_KEY")
xero_private_key = rmshelper.get_secret(xero_secret_name, region_name)
x = rmshelper.XeroRMS(xero_consumer_key, xero_private_key)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    # logging.debug([xero_consumer_key, xero_private_key])
    contacts = x.xero.contacts.filter(since=datetime(2019, 7, 1))
    for contact in contacts:
        logging.debug(contact)
    logging.debug(type(contacts))
    # invoice_id = sys.argv[1]
    # logging.debug(sys.argv)
    # logging.debug("invoice_id")
    # event = {"opportunity_id": str(3647)}
    # quick_invoice(event)
    # logging.debug(rmshelper_secret)

