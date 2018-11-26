import logging
import requests
import json


class Manager:
    def __init__(self, name):
        pass


class RMSManager:
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

    OPPORTUNITY_KEYS_TO_CLEAN = [
        "updated_at",
        "owner",
        "member",
        "billing_address",
        "venue",
        "destination",
        "opportunity_surcharges",
    ]

    def __init__(self, subdomain, token):
        # Creation of headers using subdomain and token for Requests
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
                    r = requests.get(formatted_url, headers=self.headers)
                    logging.info(f"Status Code {r.status_code}")
                    return json.loads(r.text)

                return get_json

            if method == "put":

                def put_json(id, payload):
                    """ Put requests method, reponds with Status Code """

                    def opportunity_cleaner(keys, opportunity):
                        opportunity.pop("meta")
                        for key in keys:
                            opportunity["opportunity"].pop(key)

                    formatted_url = url.format(id=str(id))
                    # Clean Opportunity keys so RMS will not Error 500
                    opportunity_cleaner(self.OPPORTUNITY_KEYS_TO_CLEAN, payload)
                    r = requests.put(formatted_url, headers=self.headers, json=payload)
                    return r

                return put_json

        name = method.lower() + "_" + key
        setattr(self, name, wrapper(name, uri, method))

    def post_invoice(self, opportunity_id, issue=True, post=True):
        """ Creates a standard invoice using inbuilt RMS method 
        Returns invoice as JSON object"""
        payload = {
            "opportunity_id": opportunity_id,
            "group_by": 0,  # Invoice grouped by items
            "part_invoice_type": 0,  # 0 = Standard Invoice type
            "invoice": {"owned_by": 1},
        }
        url = f"{self.BASE_URL}/invoices"
        logging.debug(url)
        handle = requests.post(url, headers=self.headers, json=payload)
        logging.info(f"Creating Invoice. Status code: {handle.status_code}")
        json_object = handle.json()
        invoice_id = json_object["invoice"]["id"]
        # pylint: disable=E1101
        self.get_issue_invoice(invoice_id)
        url = f"{self.BASE_URL}/invoices/{invoice_id}/post"
        logging.debug(url)
        handle = requests.post(url, headers=self.headers)
        logging.debug(handle.status_code)
        return handle

    def toggle_opportunity_invoiced_status(self, opportunity_id, override=None):
        # pylint: disable=E1101
        opportunity = self.get_opportunity(opportunity_id)
        if override == None:
            x = opportunity["opportunity"]["invoiced"]
            opportunity["opportunity"]["invoiced"] = not x
        if override == True or False:
            opportunity["opportunity"]["invoiced"] = override
        # pylint: disable=E1101
        opportunity = self.put_opportunity(opportunity_id, opportunity)
        return opportunity
