import rmshelper.rmshelper as rmshelper


def quick_invoice(event, context):
    invoice = rmshelper.quick_invoice(event["opportunity_id"])
    if invoice["post_invoice_status_code"] == 200:
        return {"statusCode": 200, "body": invoice}
    # TODO: Raise exceptions


if __name__ == "__main__":
    print("Helloworld!")
    # while True:
    #     invoice_id = input("Enter Invoice ID: ")
    #     if invoice_id == None:
    #         break
    #     event = {"opportunity_id": str(invoice_id)}
    #     quick_invoice(event, None)
