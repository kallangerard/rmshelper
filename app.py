from flask import Flask
from flask import jsonify

import rmshelper.rmshelper as rmshelper

app = Flask(__name__)


@app.route("/quick_invoice/<int:opportunity_id>/")
def quick_invoice(opportunity_id):
    invoice = rmshelper.quick_invoice(opportunity_id)
    if invoice["post_invoice_status_code"] == 200:
        resp = jsonify(invoice)
        resp.status_code = 200
        return resp


if __name__ == "__main__":
    app.run(debug=True)
