from flask import Flask
from flask import jsonify

import rmshelper.rmshelper as rmshelper

api = Flask(__name__)


@api.route("/quick_invoice/<int:opportunity_id>/", methods=["GET"])
def quick_invoice(opportunity_id):
    invoice = rmshelper.quick_invoice(opportunity_id)
    if invoice["post_invoice_status_code"] == 200:
        return jsonify(invoice), 200


if __name__ == "__main__":
    api.run(debug=True)
