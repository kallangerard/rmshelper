import rmshelper.rmshelper as rmshelper


def quick_invoice(event, context):
    invoice = rmshelper.quick_invoice(event["opportunity_id"])
    if invoice["post_invoice_status_code"] == 200:
        return {"statusCode": 200, "body": invoice}
    # TODO: Raise exceptions
