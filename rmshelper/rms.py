import logging


class Manager:
    def __init__(self, name):
        pass


class RMS:
    """Handler for Current RMS APIv1"""

    BASE_URL = "https://api.current-rms.com/api/v1"
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
        """for every item in the GET dictionary, create an object to handle GET json"""
        for key, uri in self.GET_DICTIONARY.items():
            name = "get_" + key
            logging.debug(name)
            logging.debug(uri)
            setattr(self, name, Manager._wrapper(name, uri))

    class Manager(RMS):
        def _wrapper(self, name, uri):
            self.url = self.BASE_URL + uri
            # self.name = name
            logging.debug(f"Manager = {name}")

            def get_json(id):
                logging.debug(f"{self} has URL {self.url} with ID {id}")

            self.name = get_json(id)


def Main():
    rms = RMS()
    # rms.get_opportunity("33")
    # logging.debug(rms.get_opportunity.format(id=id))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    Main()
