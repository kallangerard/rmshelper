import unittest
import calc
import os
import sys


# Prepend ../ to PYTHONPATH so that we can import RMSHelper from there.
TESTS_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.realpath(os.path.join(TESTS_ROOT, "..")))

import rmshelper


class TestAuthentication(unittest.TestCase):
    def test_get_secret(self):
        secret = rmshelper.get_secret()
        print(secret)
