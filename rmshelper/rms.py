import logging
import requests
import json


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
    PUT_DICTIONARY = {"opportunity": "/opportunities/{id}"}

    def __init__(self, subdomain, token):

        self.headers = {"X-SUBDOMAIN": subdomain, "X-AUTH-TOKEN": token}
        """for every item in the GET dictionary, create an object to handle GET json"""
        for key, uri in self.GET_DICTIONARY.items():
            self._method_iterator("get", key, uri)
        """for every item in the PUT dictionary, create an object to handle PUT json"""
        for key, uri in self.PUT_DICTIONARY.items():
            self._method_iterator("put", key, uri)

    def _method_iterator(self, method, key, uri):
        def wrapper(name, uri, method):
            """Wrapper used to distribute calls to appropriate JSON method"""
            url = self.BASE_URL + uri

            if method == "get":

                def get_json(id):
                    # Placeholder for eventual JSON GET function
                    formatted_url = url.format(id=str(id))
                    handle = requests.get(formatted_url, headers=self.headers)
                    return json.loads(handle.text)

                return get_json

            if method == "put":

                def put_json(id):
                    # Placeholder for eventual JSON PUT function
                    formatted_url = url.format(id=str(id))
                    response = {"url": formatted_url, "credentials": [subdomain, token]}
                    return response

                return put_json

        name = method.lower() + "_" + key
        setattr(self, name, wrapper(name, uri, method))

    def headers(self, subdomain, token):
        response = {"X-SUBDOMAIN": subdomain, "X-AUTH-TOKEN": token}
        return response


def main():
    order = RMS()
    # pylint: disable=E1101
    logging.debug(order.get_opportunity("Test Credentials", 2483))
    # pylint: disable=E1101
    logging.debug(order.put_opportunity("Test Credentials", 33))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
