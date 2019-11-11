import os
import shelve

import requests
import json

from faker import Faker
from faker.providers import address
from faker.providers import company


class Opportunity:
    '''
    opportunity = Opportunity()
    
    # Add items/products to the list for checking out
    opportunity.add_items_list(item_id, quantity)
    data = opportunity.checkout(
        subject,
        starts_at,
        ends_at,
        charge_starts_at,
        charge_ends_at,
        items_list,
        description=None
    )
    
    BASE_URL = "https://api.current-rms.com/api/v1"

    auth_token = os.getenv("RMS_AUTH_TOKEN")
    subdomain = os.getenv("RMS_SUBDOMAIN")

    headers = {
        "Content-Type" : "application/json",
        "X-AUTH-TOKEN": auth_token,
        "X-SUBDOMAIN": subdomain
        }

    r = requests.post(url = BASE_URL + "/members", data=data, headers=headers)
    
    '''
    # pylint: disable=E1101
    def __init__(self):
        self.items_list = None

    def opportunity_checkout(
        self,
        subject,
        starts_at,
        charge_starts_at,
        charge_ends_at,
        ends_at,
        items_list,
        description=None,
    ):
        self.checkout = {
            "opportunity": {
                "subject": "test checkout API",
                "description": str(description),
                "starts_at": starts_at,
                "charge_starts_at": charge_starts_at,
                "charge_ends_at": charge_ends_at,
                "ends_at": ends_at,
                "state": 1,
                "customer_collecting": True,
                "customer_returning": True,
                "owned_by": 1,
            },
            "items": self.items_list,
        }

        return self.checkout

    def add_items_list(self, item_id, quantity):
        self.item_list.append({
            "item_id": int(item_id),
            "transaction_type": 1,
            "quantity": float(quantity),
        })


BASE_URL = "https://api.current-rms.com/api/v1"

auth_token = os.getenv("RMS_AUTH_TOKEN")
subdomain = os.getenv("RMS_SUBDOMAIN")

headers = {
    "Content-Type" : "application/json",
    "X-AUTH-TOKEN": auth_token,
    "X-SUBDOMAIN": subdomain
    }

# r = requests.post(url = BASE_URL + "/members", json=data, headers=headers)
