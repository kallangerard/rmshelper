import logging


class Manager:
    def __init__(self, name):
        pass


class RMS:
    """Handler for Current RMS APIv1"""

    GET_DICTIONARY = {
        "invoice": "/invoices/{id}",
        "invoices": "/invoices{?page,per_page,filtermode,view_id}",
        "issue_invoice": "/invoices/{id}/issue",
        "mark_invoice_paid": "/invoices/{id}/mark_paid",
        "mark_invoice_unpaid": "/invoices/{id}/mark_unpaid",
        "void_invoice": "/invoices/{id}/void",
        "unvoid_invoice": "/invoices/{id}",
        "opportunity": "/opportunities/{id}",
        "clone_opportunity": "/opportunities/{id}/clone",
        "opportunities": "/opportunities{?page,per_page,filtermode,view_id}",
        "opportunity_convert_to_quote": "/opportunities/{id}/convert_to_quote",
        "opportunity_convert_to_order": "/opportunities/{id}/convert_to_order",
        "opportunity_revert_to_quote": "/opportunities/{id}/revert_to_quote",
    }

    def __init__(self):
        self.BASE_URL = "https://api.current-rms.com/api/v1"
        pass

    def get(self):
        """for every item in the GET dictionary, create an object to handle GET json"""
        for key, uri in self.GET_DICTIONARY.items():
            name = "get_" + key
            setattr(self, name, self.test_method(uri))

    def test_method(self, uri):
        url = self.BASE_URL + uri
        # logging.debug(self)
        # logging.debug(url)


def Main():
    rms = RMS()
    rms.get()
    print(rms.get_opportunity)
    # logging.debug(rms.get_opportunity.format(id=id))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    Main()
