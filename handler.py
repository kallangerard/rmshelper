import rmshelper.rmshelper as rmshelper


def quick_invoice(event, context):
    invoice = rmshelper.quick_invoice(event["opportunity_id"])
    if invoice["post_invoice_status_code"] == 200:
        return {"statusCode": 200, "body": invoice}
    # TODO: Raise exceptions


if __name__ == "__main__":
    while True:
        opportunity_id = input("Enter Opportunity Number: ")
        if opportunity_id == "":
            break
        # try:
        quick_invoice(str(opportunity_id), context=None)
        # except:
        # print(f"Could not invoice opportunity # {opportunity_id}")

