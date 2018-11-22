import requests
import json
import os
import logging
from xero import Xero
from xero.auth import PublicCredentials
from secretmanager import get_secret

secret_name = os.environ.get("STAGE") + "/" + "rmshelper"
region_name = os.environ.get("AWS_REGION_NAME")
try:
    secret = get_secret(secret_name, region_name)
except:
    logging.info(f"Function get_secret failed")


class RMSHelper:
    def __init__(self):
        pass


def main():
    pass


if __name__ == "__main__":
    main()
