import rmshelper.rmshelper as rmshelper


def quick_invoice(event, context):
    opportunity_id = event["pathParameters"]["opportunity_id"]
    invoice = rmshelper.quick_invoice(opportunity_id)
    if invoice["post_invoice_status_code"] == 200:
        return {"statusCode": 200, "body": invoice}


if __name__ == "__main__":
    while True:
        invoice_id = input("Enter Invoice ID: ")
        if invoice_id == None:
            break
        event = {"opportunity_id": str(invoice_id)}
        quick_invoice(event, None)
