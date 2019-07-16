import json
import logging
import os
import sys

from flask import Flask, request
from flask_restplus import Api, Resource

from rmshelper import rmshelper

app = Flask(__name__)
api = Api(app)

STAGE = os.environ.get("STAGE")
logging.debug(f"Stage: {STAGE}")

# Get RMS Secret
region_name = os.environ.get("AWS_DEFAULT_REGION")
logging.debug(f"Region: {region_name}")
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


@api.route("/opportunities/<int:opportunity_id>/quick_invoice")
class QuickInvoice(Resource):
    def post(self, opportunity_id):
        invoice = rmshelper.quick_invoice(opportunity_id, r, x)
        return {
            "opportunity_id": opportunity_id,
            "invoice_number": invoice["xero_invoice_number"],
            "status_code": invoice["post_invoice_status_code"],
        }


@api.route("/invoices/<xero_invoice_uuid>/Email")
class EmailInvoice(Resource):
    def post(self, xero_invoice_uuid):
        email = x.email_invoice(xero_invoice_uuid)
        return email.text


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True)
