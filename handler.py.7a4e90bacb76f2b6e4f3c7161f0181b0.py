import os
import sys
import logging
import json

from rmshelper import rmshelper


def quick_invoice(event, context=None):
    invoice = rmshelper.quick_invoice(event["opportunity_id"], r, x)
    if invoice["post_invoice_status_code"] == 200:
        return {"statusCode": 200, "body": invoice}
    # TODO: Raise exceptions


region_name = os.environ.get("AWS_DEFAULT_REGION")

rmshelper_secret = json.loads(
    rmshelper.get_secret(f"{os.environ.get('STAGE')}/rmshelper", region_name)
)

r = rmshelper.RMSManager(
    rmshelper_secret.get("SUBDOMAIN"), rmshelper_secret.get("RMS_TOKEN")
)

xero_consumer_key = rmshelper_secret.get("XERO_CONSUMER_KEY")
xero_private_key = rmshelper.get_secret(f"{os.environ.get('STAGE')}/xero", region_name)


x = rmshelper.XeroRMS(xero_consumer_key, xero_private_key)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.debug([xero_consumer_key, xero_private_key])
    # invoice_id = sys.argv[1]
    # logging.debug(sys.argv)
    # logging.debug("invoice_id")
    # event = {"opportunity_id": str(3647)}
    # quick_invoice(event)
    # logging.debug(rmshelper_secret)

