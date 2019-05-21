from chalice import Chalice
import chalicelib.rmshelper.rmshelper as rmshelper

app = Chalice(app_name="rmshelper")


@app.route("/quick_invoice/{opportunity_id}", methods=["GET"], api_key_required=True)
def quick_invoice(opportunity_id):
    invoice = rmshelper.quick_invoice(opportunity_id)
    if invoice["post_invoice_status_code"] == 200:
        return {"body": invoice}