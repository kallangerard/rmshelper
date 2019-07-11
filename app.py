import os
import sys
import logging
import json

from flask import Flask

from rmshelper import rmshelper


STAGE = os.environ.get("STAGE")

# Get RMS Secret
region_name = os.environ.get("AWS_DEFAULT_REGION")
secret_name = f"{STAGE}/rmshelper"
rmshelper_secret = json.loads(rmshelper.get_secret(secret_name, region_name))

# Create RMS Object
rms_subdomain = rmshelper_secret.get("SUBDOMAIN")
rms_token = rmshelper_secret.get("RMS_TOKEN")
r = rmshelper.RMSManager(rms_subdomain, rms_token)

# Create Xero Object
xero_secret_name = f"{STAGE}/xero"
xero_consumer_key = rmshelper_secret.get("XERO_CONSUMER_KEY")
xero_private_key = rmshelper.get_secret(xero_secret_name, region_name)
x = rmshelper.XeroRMS(xero_consumer_key, xero_private_key)

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route("/quick_invoice/<int:opportunity_id>", methods=["GET"])
def quick_invoice(opportunity_id):
    invoice = rmshelper.quick_invoice(opportunity_id, r, x)
    if invoice["post_invoice_status_code"] == 200:
        return f"Invoiced {invoice['xero_invoice_number']}, {invoice['post_invoice_status_code']}"
    # TODO: Raise exceptions


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app.run()
