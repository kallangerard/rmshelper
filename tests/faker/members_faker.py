import os
import shelve

import requests
import json

from faker import Faker
from faker.providers import address
from faker.providers import company


class Members:
    def create_organisation(
        self,
        organisation_name,
        organisation_street=None,
        organisation_postcode=None,
        organisation_suburb=None,
        organisation_state=None,
        organisation_email=None,
        organisation_work_phone=None,
        organisation_mobile_phone=None,
        tag_list=[],
    ):
        self.organisation = {
            "member": {
                "name": organisation_name,
                "active": True,
                "bookable": False,
                "location_type": 1,
                "locale": "en-AU",
                "membership_type": "Organisation",
                "custom_fields": {
                    "emergency_contact": "",
                    "emergency_contact_phone": "",
                },
                "primary_address": {
                    "name": organisation_name,
                    "street": organisation_street,
                    "postcode": organisation_postcode,
                    "city": organisation_suburb,
                    "county": organisation_state,
                    "country_id": 5,
                    "country_name": "Australia",
                    "type_id": 3001,
                    "address_type_name": "Primary",
                },
                "membership": {"owned_by": 1},
                "emails": [{"address": organisation_email, "type_id": 4001}],
                "phones": [
                    {
                        "number": str(organisation_work_phone),
                        "type_id": 6001,
                        "phone_type_name": "Work",
                    },
                    {
                        "number": str(organisation_mobile_phone),
                        "type_id": 6002,
                        "phone_type_name": "Mobile",
                    },
                ],
                "tag_list": tag_list,
                "links": [],
                "addresses": [],
                "service_stock_levels": [],
                "child_members": [],
                "parent_members": [],
            }
        }

        return self.organisation


class FakeGenerator:
    def __init__(self):
        self.fake = Faker()
        self.fake.add_provider(company)


class MemberGenerator(FakeGenerator):
    def create_organisation(self):
        # pylint: disable=E1101
        first_name = self.fake.first_name()
        last_name = self.fake.last_name()
        organisation_name = self.fake.company()
        organisation_email = first_name + "." + last_name + "@example.com"

        self.member = Members()

        self.member_object = self.member.create_organisation(
            organisation_name=organisation_name,
            organisation_email=organisation_email,
            tag_list=["faker"],
        )


BASE_URL = "https://api.current-rms.com/api/v1"

auth_token = os.getenv("RMS_AUTH_TOKEN")
subdomain = os.getenv("RMS_SUBDOMAIN")

headers = {
    "Content-Type": "application/json",
    "X-AUTH-TOKEN": auth_token,
    "X-SUBDOMAIN": subdomain,
}

for _ in range(5):
    try:
        org = MemberGenerator()
        org.create_organisation()
        payload = org.member_object
        r = requests.post(url=BASE_URL + "/members", json=payload, headers=headers)
    except:
        print(f"Can not create member")

